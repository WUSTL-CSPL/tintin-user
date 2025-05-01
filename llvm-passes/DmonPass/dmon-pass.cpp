#include "llvm/ADT/SmallVector.h"
#include "llvm/IR/BasicBlock.h"
#include "llvm/IR/CFG.h"  // For successors()
#include "llvm/IR/Function.h"
#include "llvm/IR/IRBuilder.h"
#include "llvm/IR/Instructions.h"
#include "llvm/IR/LegacyPassManager.h"
#include "llvm/IR/Module.h"
#include "llvm/Pass.h"
#include "llvm/Support/raw_ostream.h"
#include "llvm/Transforms/IPO/PassManagerBuilder.h"
#include "tintin-utils.h"

using namespace llvm;

namespace {
struct Hello : public ModulePass {
    static char ID;
    Hello() : ModulePass(ID) {}
    bool runOnModule(Module &M) override {
        LLVMContext &Ctx = M.getContext();
        Function *MainFn = M.getFunction("main");

        if (!MainFn) {
            errs() << "No main function found.\n";
            return false;
        }

        // Declare instrumentation functions
        FunctionCallee TintinStart = M.getOrInsertFunction(
            "tintin_start", FunctionType::get(Type::getVoidTy(Ctx), false));
        FunctionCallee TintinEnd = M.getOrInsertFunction(
            "tintin_end", FunctionType::get(Type::getVoidTy(Ctx), false));

        // Insert tintin_start at the beginning of main()
        IRBuilder<> Builder(&*MainFn->getEntryBlock().getFirstInsertionPt());
        Builder.CreateCall(TintinStart);

        // Insert tintin_end before each return
        for (BasicBlock &BB : *MainFn) {
            for (Instruction &I : BB) {
                if (isa<ReturnInst>(&I)) {
                    IRBuilder<> RetBuilder(&I);
                    RetBuilder.CreateCall(TintinEnd);
                }
            }
        }

        return true;
    }
};  // end of struct Hello
}  // end of anonymous namespace

char Hello::ID = 0;
static RegisterPass<Hello> X("func_scope", "Tintin Test Pass",
                             false /* Only looks at CFG */,
                             false /* Analysis Pass */);

static RegisterStandardPasses Y(PassManagerBuilder::EP_EarlyAsPossible,
                                [](const PassManagerBuilder &Builder,
                                   legacy::PassManagerBase &PM) {
                                    PM.add(new Hello());
                                });
