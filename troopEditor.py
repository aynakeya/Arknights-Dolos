from model.troopBuilder import troopBuilder,characterBuilder

tb = troopBuilder.init()
tb.setCharacterBuilder(characterBuilder.init())
char = []
for c in tb.cBuilder.characters.keys():
    if "char" in c and tb.cBuilder.characters[c]["obtainable"]:
        char.append(c)

for c in char:
    tb.addCharacter(c)

for key, char in tb.chars.items():
    tb.chars[key] = tb.cBuilder.graduate(tb.chars[key])
tb.save(indent=2)