from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

ASaidKnight = Symbol("A said 'I am a Knight'")
ASaidKnave = Symbol("A said 'I am a Knave'")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
sentence =  And(AKnave, AKnight)
knowledge0 = And(
    Or(AKnave, AKnight),
    Not(And(AKnight, AKnave)),

    Implication(AKnave, Not(sentence)),
    Implication(AKnight, sentence)
)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentence = And(AKnave, BKnave)
knowledge1 = And(
    Or(AKnave, AKnight),
    Not(And(AKnight, AKnave)),

    Or(BKnave, BKnight),
    Not(And(BKnight, BKnave)),

    Implication(AKnave, Not(sentence)),
    Implication(AKnight, sentence),
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentenceA = Or(And(AKnave, BKnave), And(AKnight, BKnight))
sentenceB = Or(And(AKnight, BKnave), And(BKnight, AKnave))
knowledge2 = And(
    Or(AKnave, AKnight),
    Not(And(AKnight, AKnave)),

    Or(BKnave, BKnight),
    Not(And(BKnight, BKnave)),

    Implication(AKnave, Not(sentenceA)),
    Implication(AKnight, sentenceA),

    Implication(BKnave, Not(sentenceB)),
    Implication(BKnight, sentenceB)

)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3= And(
    Not(And(AKnight, AKnave)),  
    Or(AKnight, AKnave),        

    Not(And(BKnight, BKnave)),  
    Or(BKnight, BKnave),        

    Not(And(CKnight, CKnave)),  
    Or(CKnight, CKnave),        

    Or(
        And(
            Implication(AKnight, AKnight),
            Implication(AKnave, Not(AKnight))
        ),
        
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )
    ),

    Not(And(
        And(
            Implication(AKnight, AKnight),
            Implication(AKnave, Not(AKnight))
        ),
        
        And(
            Implication(AKnight, AKnave),
            Implication(AKnave, Not(AKnave))
        )
    )),

    Implication(BKnight, And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    )),

    Implication(BKnave, Not(And(
        Implication(AKnight, AKnave),
        Implication(AKnave, Not(AKnave))
    ))),


    Implication(BKnight, CKnave),
    Implication(BKnave, Not(CKnave)),

    Implication(CKnight, AKnight),
    Implication(CKnave, Not(AKnight))
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")
    print(model_check(knowledge3, AKnight))


if __name__ == "__main__":
    main()
