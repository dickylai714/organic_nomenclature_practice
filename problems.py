# @title Question Bank
# You can put your massive list of questions here!
practice_problems = [
    # === Straight-chain Alkane ===
    {"smiles": "C", "name": "methane", "condensed": "CH4", "category": "Straight-chain Alkane", "difficulty": "Easy"},
    {"smiles": "CC", "name": "ethane", "condensed": "CH3CH3", "category": "Straight-chain Alkane", "difficulty": "Easy"},
    {"smiles": "CCC", "name": "propane", "condensed": "CH3CH2CH3", "category": "Straight-chain Alkane", "difficulty": "Easy"},
    {"smiles": "CCCC", "name": "butane", "condensed": "CH3CH2CH2CH3", "category": "Straight-chain Alkane", "difficulty": "Medium"},
    {"smiles": "CCCCC", "name": "pentane", "condensed": "CH3(CH2)3CH3", "category": "Straight-chain Alkane", "difficulty": "Medium"},
    {"smiles": "CCCCCC", "name": "hexane", "condensed": "CH3(CH2)4CH3", "category": "Straight-chain Alkane", "difficulty": "Medium"},
    {"smiles": "CCCCCCC", "name": "heptane", "condensed": "CH3(CH2)5CH3", "category": "Straight-chain Alkane", "difficulty": "Hard"},
    {"smiles": "CCCCCCCC", "name": "octane", "condensed": "CH3(CH2)6CH3", "category": "Straight-chain Alkane", "difficulty": "Hard"},

    # === Branched Alkane ===
    {"smiles": "CC(C)C", "name": "2-methylpropane", "condensed": "CH3CH(CH3)CH3", "category": "Branched Alkane", "difficulty": "Easy", "alternative_names": ["methylpropane"]},
    {"smiles": "CC(C)CC", "name": "2-methylbutane", "condensed": "CH3CH(CH3)CH2CH3", "category": "Branched Alkane", "difficulty": "Medium"},
    {"smiles": "CCC(C)CC", "name": "3-methylpentane", "condensed": "CH3CH2CH(CH3)CH2CH3", "category": "Branched Alkane", "difficulty": "Medium"},
    {"smiles": "CC(C)(C)C", "name": "2,2-dimethylpropane", "condensed": "C(CH3)4", "category": "Branched Alkane", "difficulty": "Medium"},
    {"smiles": "CC(C)CCC", "name": "2-methylpentane", "condensed": "CH3CH(CH3)CH2CH2CH3", "category": "Branched Alkane", "difficulty": "Medium"},
    {"smiles": "CC(C)C(C)C", "name": "2,3-dimethylbutane", "condensed": "CH3CH(CH3)CH(CH3)CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    {"smiles": "CCC(C)(C)CC", "name": "3,3-dimethylpentane", "condensed": "CH3CH2C(CH3)2CH2CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    {"smiles": "CC(C)CC(C)C", "name": "2,4-dimethylpentane", "condensed": "CH3CH(CH3)CH2CH(CH3)CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    {"smiles": "CCC(CC)CCC", "name": "3-ethylhexane", "condensed": "CH3CH2CH2CH(CH2CH3)CH2CH2CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    {"smiles": "CC(C)(C)CC(C)C", "name": "2,2,4-trimethylpentane", "condensed": "(CH3)3CCH2CH(CH3)CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    # === Branched Alkane (Continued) ===
    {"smiles": "CC(C)(C)CC", "name": "2,2-dimethylbutane", "condensed": "(CH3)3CCH2CH3", "category": "Branched Alkane", "difficulty": "Medium"},
    {"smiles": "CC(C)C(C)CC", "name": "2,3-dimethylpentane", "condensed": "CH3CH(CH3)CH(CH3)CH2CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    {"smiles": "CCC(CC)CC", "name": "3-ethylpentane", "condensed": "CH3CH2CH(CH2CH3)CH2CH3", "category": "Branched Alkane", "difficulty": "Medium"},
    {"smiles": "CC(C)C(CC)CC", "name": "3-ethyl-2-methylpentane", "condensed": "CH3CH(CH3)CH(CH2CH3)CH2CH3", "category": "Branched Alkane", "difficulty": "Hard"},
    {"smiles": "CCC(C)(C)C(CC)CCC", "name": "4-ethyl-3,3-dimethylheptane", "condensed": "CH3CH2C(CH3)2CH(CH2CH3)CH2CH2CH3", "category": "Branched Alkane", "difficulty": "Hard"},

    # === Alkene === (Includes straight and branched)
    {"smiles": "C=C", "name": "ethene", "condensed": "CH2=CH2", "category": "Alkene", "difficulty": "Easy"},
    {"smiles": "CC=C", "name": "propene", "condensed": "CH3CH=CH2", "category": "Alkene", "difficulty": "Easy"},
    {"smiles": "C=CCC", "name": "but-1-ene", "condensed": "CH2=CHCH2CH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "CC=CC", "name": "but-2-ene", "condensed": "CH3CH=CHCH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "C=CCCC", "name": "pent-1-ene", "condensed": "CH2=CHCH2CH2CH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "CC=CCC", "name": "pent-2-ene", "condensed": "CH3CH=CHCH2CH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "CC(C)C=C", "name": "3-methylbut-1-ene", "condensed": "CH3CH(CH3)CH=CH2", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "C=C(C)CC", "name": "2-methylbut-1-ene", "condensed": "CH2=C(CH3)CH2CH3", "category": "Alkene", "difficulty": "Hard"},
    {"smiles": "CC=C(C)C", "name": "2-methylbut-2-ene", "condensed": "CH3CH=C(CH3)CH3", "category": "Alkene", "difficulty": "Hard"},
    {"smiles": "CCC(C)=CCC", "name": "3-methylhex-3-ene", "condensed": "CH3CH2C(CH3)=CHCH2CH3", "category": "Alkene", "difficulty": "Hard"},
    
    # === Alkene (Continued) ===
    {"smiles": "C=CCCCC", "name": "hex-1-ene", "condensed": "CH2=CHCH2CH2CH2CH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "CC=CCCC", "name": "hex-2-ene", "condensed": "CH3CH=CHCH2CH2CH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "CCC=CCC", "name": "hex-3-ene", "condensed": "CH3CH2CH=CHCH2CH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "C=CC(C)CC", "name": "3-methylpent-1-ene", "condensed": "CH2=CHCH(CH3)CH2CH3", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "CC=CC(C)C", "name": "4-methylpent-2-ene", "condensed": "CH3CH=CHCH(CH3)CH3", "category": "Alkene", "difficulty": "Medium"}, # Note: Could be (E) or (Z)
    {"smiles": "CC(C)=C(C)C", "name": "2,3-dimethylbut-2-ene", "condensed": "CH3C(CH3)=C(CH3)CH3", "category": "Alkene", "difficulty": "Hard"},
    
    # Dienes
    {"smiles": "C=CC=C", "name": "buta-1,3-diene", "condensed": "CH2=CHCH=CH2", "category": "Alkene", "difficulty": "Medium"},
    {"smiles": "C=CC=CC", "name": "penta-1,3-diene", "condensed": "CH2=CHCH=CHCH3", "category": "Alkene", "difficulty": "Hard"}, # Note: CH3 end can be E/Z
    {"smiles": "C=CCC=C", "name": "penta-1,4-diene", "condensed": "CH2=CHCH2CH=CH2", "category": "Alkene", "difficulty": "Hard"},
    {"smiles": "C=C(C)C=C", "name": "2-methylbuta-1,3-diene", "condensed": "CH2=C(CH3)CH=CH2", "category": "Alkene", "difficulty": "Hard", "alternative_names": ["isoprene"]},
    
    # === Haloalkane ===
    {"smiles": "C(Cl)", "name": "chloromethane", "condensed": "CH3Cl", "category": "Haloalkane", "difficulty": "Easy"},
    {"smiles": "CCBr", "name": "bromoethane", "condensed": "CH3CH2Br", "category": "Haloalkane", "difficulty": "Easy"},
    {"smiles": "CI", "name": "iodomethane", "condensed": "CH3I", "category": "Haloalkane", "difficulty": "Easy"}, # Added Iodo
    {"smiles": "CF", "name": "fluoromethane", "condensed": "CH3F", "category": "Haloalkane", "difficulty": "Easy"},
    {"smiles": "CCCI", "name": "1-iodopropane", "condensed": "CH3CH2CH2I", "category": "Haloalkane", "difficulty": "Medium"}, # Added Iodo
    {"smiles": "CC(I)C", "name": "2-iodopropane", "condensed": "CH3CHICH3", "category": "Haloalkane", "difficulty": "Medium"}, # Added Iodo
    {"smiles": "CCCCl", "name": "1-chloropropane", "condensed": "CH3CH2CH2Cl", "category": "Haloalkane", "difficulty": "Medium"},
    {"smiles": "CC(Cl)C", "name": "2-chloropropane", "condensed": "CH3CHClCH3", "category": "Haloalkane", "difficulty": "Medium"},
    {"smiles": "C(F)(F)F", "name": "trifluoromethane", "condensed": "CHF3", "category": "Haloalkane", "difficulty": "Medium"},
    {"smiles": "CC(Br)CC", "name": "2-bromobutane", "condensed": "CH3CHBrCH2CH3", "category": "Haloalkane", "difficulty": "Medium"},
    {"smiles": "ClCCBr", "name": "1-bromo-2-chloroethane", "condensed": "ClCH2CH2Br", "category": "Haloalkane", "difficulty": "Hard"},
    {"smiles": "CC(Cl)(I)C", "name": "2-chloro-2-iodopropane", "condensed": "CH3C(Cl)(I)CH3", "category": "Haloalkane", "difficulty": "Hard"}, # Added Iodo
    {"smiles": "FC(Cl)I", "name": "chlorofluoroiodomethane", "condensed": "CHFClI", "category": "Haloalkane", "difficulty": "Hard"}, # Added Iodo
    
    # === Haloalkane (Continued) ===
    {"smiles": "CC(C)CBr", "name": "1-bromo-2-methylpropane", "condensed": "CH3CH(CH3)CH2Br", "category": "Haloalkane", "difficulty": "Medium"},
    {"smiles": "CC(Cl)C(C)C", "name": "2-chloro-3-methylbutane", "condensed": "CH3CH(Cl)CH(CH3)CH3", "category": "Haloalkane", "difficulty": "Hard"},
    {"smiles": "ClCC(C)(C)C", "name": "1-chloro-2,2-dimethylpropane", "condensed": "ClCH2C(CH3)3", "category": "Haloalkane", "difficulty": "Hard"},
    {"smiles": "FC(Br)(Cl)C", "name": "1-bromo-1-chloro-1-fluoroethane", "condensed": "CH3CBrClF", "category": "Haloalkane", "difficulty": "Hard"}, # Halogens listed alphabetically
    {"smiles": "CC(F)C(Cl)C", "name": "2-chloro-3-fluorobutane", "condensed": "CH3CH(F)CH(Cl)CH3", "category": "Haloalkane", "difficulty": "Hard"}, # Alphabetical chloro, then fluoro
    
    # === Alkanol ===
    {"smiles": "CO", "name": "methanol", "condensed": "CH3OH", "category": "Alkanol", "difficulty": "Easy"},
    {"smiles": "CCO", "name": "ethanol", "condensed": "CH3CH2OH", "category": "Alkanol", "difficulty": "Easy"},
    {"smiles": "CCCO", "name": "propan-1-ol", "condensed": "CH3CH2CH2OH", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "CC(O)C", "name": "propan-2-ol", "condensed": "CH3CH(OH)CH3", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "CCCCO", "name": "butan-1-ol", "condensed": "CH3CH2CH2CH2OH", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "CC(O)CC", "name": "butan-2-ol", "condensed": "CH3CH(OH)CH2CH3", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "CC(C)(O)C", "name": "2-methylpropan-2-ol", "condensed": "(CH3)3COH", "category": "Alkanol", "difficulty": "Hard","alternative_names": ["methylpropan-2-ol"]},
    {"smiles": "CC(C)CO", "name": "2-methylpropan-1-ol", "condensed": "CH3CH(CH3)CH2OH", "category": "Alkanol", "difficulty": "Hard","alternative_names": ["methylpropan-1-ol"]},
    {"smiles": "CCC(O)CC", "name": "pentan-3-ol", "condensed": "CH3CH2CH(OH)CH2CH3", "category": "Alkanol", "difficulty": "Hard"},
    {"smiles": "CC(O)C(O)C", "name": "butane-2,3-diol", "condensed": "CH3CH(OH)CH(OH)CH3", "category": "Alkanol", "difficulty": "Hard"},
    # === Alkanol (Continued) ===
    {"smiles": "CCCCCCO", "name": "hexan-1-ol", "condensed": "CH3(CH2)4CH2OH", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "CCCC(O)CC", "name": "hexan-3-ol", "condensed": "CH3CH2CH2CH(OH)CH2CH3", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "CC(C)CCO", "name": "3-methylbutan-1-ol", "condensed": "CH3CH(CH3)CH2CH2OH", "category": "Alkanol", "difficulty": "Hard"},
    {"smiles": "CC(O)C(C)C", "name": "3-methylbutan-2-ol", "condensed": "CH3CH(OH)CH(CH3)CH3", "category": "Alkanol", "difficulty": "Hard"},
    {"smiles": "OCCCO", "name": "propane-1,3-diol", "condensed": "HOCH2CH2CH2OH", "category": "Alkanol", "difficulty": "Medium"},
    {"smiles": "OCC(O)CO", "name": "propane-1,2,3-triol", "condensed": "HOCH2CH(OH)CH2OH", "category": "Alkanol", "difficulty": "Hard", "alternative_names": ["glycerol"]},

    # === Carboxylic Acid ===
    {"smiles": "C(=O)O", "name": "methanoic acid", "condensed": "HCOOH", "category": "Carboxylic Acid", "difficulty": "Easy"},
    {"smiles": "CC(=O)O", "name": "ethanoic acid", "condensed": "CH3COOH", "category": "Carboxylic Acid", "difficulty": "Easy"},
    {"smiles": "CCC(=O)O", "name": "propanoic acid", "condensed": "CH3CH2COOH", "category": "Carboxylic Acid", "difficulty": "Medium"},
    {"smiles": "CCCC(=O)O", "name": "butanoic acid", "condensed": "CH3CH2CH2COOH", "category": "Carboxylic Acid", "difficulty": "Medium"},
    {"smiles": "CC(C)C(=O)O", "name": "2-methylpropanoic acid", "condensed": "CH3CH(CH3)COOH", "category": "Carboxylic Acid", "difficulty": "Medium"},
    {"smiles": "CCCCC(=O)O", "name": "pentanoic acid", "condensed": "CH3CH2CH2CH2COOH", "category": "Carboxylic Acid", "difficulty": "Hard"},
    {"smiles": "CC(C)CC(=O)O", "name": "3-methylbutanoic acid", "condensed": "CH3CH(CH3)CH2COOH", "category": "Carboxylic Acid", "difficulty": "Hard"},
    {"smiles": "C(C(=O)O)C(=O)O", "name": "propanedioic acid", "condensed": "HOOCCH2COOH", "category": "Carboxylic Acid", "difficulty": "Hard"},
    {"smiles": "CC(Cl)C(=O)O", "name": "2-chloropropanoic acid", "condensed": "CH3CH(Cl)COOH", "category": "Carboxylic Acid", "difficulty": "Hard"}, # Also Mixed
    # === Carboxylic Acid (Continued) ===
    {"smiles": "CCCCCC(=O)O", "name": "hexanoic acid", "condensed": "CH3(CH2)4COOH", "category": "Carboxylic Acid", "difficulty": "Hard"},
    {"smiles": "CCC(CC)C(=O)O", "name": "2-ethylbutanoic acid", "condensed": "CH3CH2CH(CH2CH3)COOH", "category": "Carboxylic Acid", "difficulty": "Hard"},
    {"smiles": "CC(C)(C)C(=O)O", "name": "2,2-dimethylpropanoic acid", "condensed": "(CH3)3CCOOH", "category": "Carboxylic Acid", "difficulty": "Hard", "alternative_names": ["pivalic acid"]},
    {"smiles": "O=C(O)CCC(=O)O", "name": "butanedioic acid", "condensed": "HOOC(CH2)2COOH", "category": "Carboxylic Acid", "difficulty": "Hard", "alternative_names": ["succinic acid"]},
    {"smiles": "O=C(O)CCCC(=O)O", "name": "pentanedioic acid", "condensed": "HOOC(CH2)3COOH", "category": "Carboxylic Acid", "difficulty": "Hard", },
    
    # === Mixed Functional Groups === (Focusing on combinations taught in S4, avoiding primary ketones)
    # Alkanol + Alkene
    {"smiles": "CC(O)C=C", "name": "but-3-en-2-ol", "condensed": "CH2=CHCH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "C=CCCO", "name": "but-3-en-1-ol", "condensed": "CH2=CHCH2CH2OH", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "CC=CC(O)C", "name": "pent-3-en-2-ol", "condensed": "CH3CH=CHCH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "C=C(C)CO", "name": "2-methylprop-2-en-1-ol", "condensed": "CH2=C(CH3)CH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # Alkanol + Haloalkane
    {"smiles": "OCCBr", "name": "2-bromoethanol", "condensed": "HOCH2CH2Br", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "ClCC(O)C", "name": "1-chloropropan-2-ol", "condensed": "ClCH2CH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "CC(O)CI", "name": "1-iodopropan-2-ol", "condensed": "ICH2CH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Added iodo
    {"smiles": "C=CC(Br)CO", "name": "2-bromobut-3-en-1-ol", "condensed": "CH2=CHCH(Br)CH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # Alkene + Haloalkane
    {"smiles": "C=CCl", "name": "chloroethene", "condensed": "CH2=CHCl", "category": "Mixed Functional Groups", "difficulty": "Easy"},
    {"smiles": "BrC=C", "name": "bromoethene", "condensed": "CHBr=CH2", "category": "Mixed Functional Groups", "difficulty": "Easy"},
    {"smiles": "C=CI", "name": "iodoethene", "condensed": "CH2=CHI", "category": "Mixed Functional Groups", "difficulty": "Easy"}, # Added iodo
    {"smiles": "ClC=CCl", "name": "1,2-dichloroethene", "condensed": "CHCl=CHCl", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "C=CCBr", "name": "3-bromoprop-1-ene", "condensed": "CH2=CHCH2Br", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    # Haloalkene (More examples)
    {"smiles": "ClC=CCCl", "name": "1,3-dichloropropene", "condensed": "ClCH=CHCH2Cl", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Can be E/Z
    {"smiles": "C=C(Br)CBr", "name": "2,3-dibromoprop-1-ene", "condensed": "CH2=C(Br)CH2Br", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # Carboxylic Acid + Alkene (Unsaturated Acids)
    {"smiles": "C=CC(=O)O", "name": "propenoic acid", "condensed": "CH2=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "CC=CC(=O)O", "name": "but-2-enoic acid", "condensed": "CH3CH=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "C=C(C)C(=O)O", "name": "2-methylpropenoic acid", "condensed": "CH2=C(CH3)COOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # Carboxylic Acid + Haloalkane (Halo Acids)
    {"smiles": "ClCC(=O)O", "name": "chloroethanoic acid", "condensed": "ClCH2COOH", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "BrCCC(=O)O", "name": "3-bromopropanoic acid", "condensed": "BrCH2CH2COOH", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "CC(I)C(=O)O", "name": "2-iodopropanoic acid", "condensed": "CH3CH(I)COOH", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Added iodo
    {"smiles": "ClC(Cl)C(=O)O", "name": "2,2-dichloroethanoic acid", "condensed": "Cl2CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # Carboxylic Acid + Alkene + Halo
    {"smiles": "ClC=CC(=O)O", "name": "3-chloropropenoic acid", "condensed": "ClCH=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Hard", "alternative_names": ["3-chloroprop-2-enoic acid"]}, # Can be E/Z
    {"smiles": "C=C(Cl)C(=O)O", "name": "2-chloropropenoic acid", "condensed": "CH2=C(Cl)COOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "BrCC=CC(=O)O", "name": "4-bromobut-2-enoic acid", "condensed": "BrCH2CH=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Can be E/Z

    # Alkanol + Alkene + Halo (More examples)
    {"smiles": "ClCC(O)C=C", "name": "1-chlorobut-3-en-2-ol", "condensed": "CH2=CHCH(OH)CH2Cl", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Typo in thought process, CH2=CHCH(OH)CH2Cl is correct for this name
    {"smiles": "C=CCC(O)CI", "name": "5-iodopent-1-en-4-ol", "condensed": "CH2=CHCH2CH(OH)CH2I", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    
    # More challenging combinations without primary ketones
    {"smiles": "ClC=CC(O)C", "name": "1-chlorobut-1-en-3-ol", "condensed": "ClCH=CHCH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "CC(Br)=CC(=O)O", "name": "3-bromobut-2-enoic acid", "condensed": "CH3C(Br)=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "OCC(Cl)C=C", "name": "2-chlorobut-3-en-1-ol", "condensed": "HOCH2CH(Cl)CH=CH2", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "C=C(Cl)C(C)(O)C", "name": "3-chloro-2-methylbut-3-en-2-ol", "condensed": "CH2=C(Cl)C(CH3)(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Corrected from before
    {"smiles": "BrC(C)=CC(O)C", "name": "4-bromopent-3-en-2-ol", "condensed": "BrCH(CH3)CH=CHCH(OH)CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"},

    # Additional Mixed Examples
    {"smiles": "CCC(O)C=C", "name": "pent-1-en-3-ol", "condensed": "CH3CH2CH(OH)CH=CH2", "category": "Mixed Functional Groups", "difficulty": "Medium"},
    {"smiles": "CC(Cl)C(O)CC", "name": "2-chloropentan-3-ol", "condensed": "CH3CH(Cl)CH(OH)CH2CH3", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "C=C(Br)CCC(=O)O", "name": "4-bromopent-4-enoic acid", "condensed": "CH2=C(Br)CH2CH2COOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "OCC=CCO", "name": "but-2-ene-1,4-diol", "condensed": "HOCH2CH=CHCH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "ClCC(Cl)CO", "name": "2,3-dichloropropan-1-ol", "condensed": "ClCH2CH(Cl)CH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "C=CC(Br)CO", "name": "2-bromobut-3-en-1-ol", "condensed": "CH2=CHCH(Br)CH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "CC(Cl)=CCC(=O)O", "name": "4-chloropent-3-enoic acid", "condensed": "CH3C(Cl)=CHCH2COOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    {"smiles": "CC(I)C=C", "name": "3-iodobut-1-ene", "condensed": "CH3CH(I)CH=CH2", "category": "Mixed Functional Groups", "difficulty": "Hard"}, # Alkene double bond gets lower number if choice
    {"smiles": "O=C(O)C=CC(=O)O", "name": "butenedioic acid", "condensed": "HOOCCH=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    
    # === Dienes (Focusing on the addition of "a" to the parent chain) ===
    {"smiles": "C=CC=CCCC", "name": "hexa-1,3-diene", "condensed": "CH2=CHCH=CHCH2CH3", "category": "Alkene", "difficulty": "Hard"},
    {"smiles": "C=CCCCC=C", "name": "hexa-1,5-diene", "condensed": "CH2=CHCH2CH2CH=CH2", "category": "Alkene", "difficulty": "Hard"},
    {"smiles": "CC=CC=CC", "name": "hexa-2,4-diene", "condensed": "CH3CH=CHCH=CHCH3", "category": "Alkene", "difficulty": "Hard"},
    {"smiles": "C=C(C)C(C)=C", "name": "2,3-dimethylbuta-1,3-diene", "condensed": "CH2=C(CH3)C(CH3)=CH2", "category": "Alkene", "difficulty": "Hard"},

    # === Diols (Focusing on retaining the "e" in the alkane parent name) ===
    {"smiles": "OCCCCCO", "name": "pentane-1,5-diol", "condensed": "HOCH2CH2CH2CH2CH2OH", "category": "Alkanol", "difficulty": "Hard"},
    {"smiles": "OCCCCCCO", "name": "hexane-1,6-diol", "condensed": "HOCH2(CH2)4CH2OH", "category": "Alkanol", "difficulty": "Hard"},
    {"smiles": "CC(O)CCC(O)C", "name": "hexane-2,5-diol", "condensed": "CH3CH(OH)CH2CH2CH(OH)CH3", "category": "Alkanol", "difficulty": "Hard"},
    {"smiles": "OCC(C)CCO", "name": "2-methylbutane-1,4-diol", "condensed": "HOCH2CH(CH3)CH2CH2OH", "category": "Alkanol", "difficulty": "Hard"},

    # === Dioic Acids (Focusing on retaining the "e" in the alkane parent name) ===
    {"smiles": "O=C(O)CCCCC(=O)O", "name": "hexanedioic acid", "condensed": "HOOC(CH2)4COOH", "category": "Carboxylic Acid", "difficulty": "Hard", "alternative_names": ["adipic acid"]},
    {"smiles": "O=C(O)CC(C)C(=O)O", "name": "2-methylbutanedioic acid", "condensed": "HOOCCH2CH(CH3)COOH", "category": "Carboxylic Acid", "difficulty": "Hard"},
    {"smiles": "O=C(O)C(C)(C)C(=O)O", "name": "2,2-dimethylpropanedioic acid", "condensed": "HOOCC(CH3)2COOH", "category": "Carboxylic Acid", "difficulty": "Hard"},

    # === Mixed Difficult Cases (Testing multiple consonant/vowel rules simultaneously) ===
    # Here, "ene" retains its "e" because "diol" starts with a "d"
    {"smiles": "OCC=CC=CCO", "name": "hexa-2,4-diene-1,6-diol", "condensed": "HOCH2CH=CHCH=CHCH2OH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    # Here, "ene" retains its "e" because "dioic acid" starts with a "d"
    {"smiles": "O=C(O)C=CC=CC(=O)O", "name": "hexa-2,4-dienedioic acid", "condensed": "HOOCCH=CHCH=CHCOOH", "category": "Mixed Functional Groups", "difficulty": "Hard"},
    
     # === S5 Placeholders ===
# === Aldehyde & Ketone ===
    {"smiles": "C=O", "name": "methanal", "condensed": "HCHO", "category": "Aldehyde & Ketone", "difficulty": "Easy", "alternative_names": ["formaldehyde"]},
    {"smiles": "CC=O", "name": "ethanal", "condensed": "CH3CHO", "category": "Aldehyde & Ketone", "difficulty": "Easy", "alternative_names": ["acetaldehyde"]},
    {"smiles": "CCC=O", "name": "propanal", "condensed": "CH3CH2CHO", "category": "Aldehyde & Ketone", "difficulty": "Medium"},
    {"smiles": "CCCC=O", "name": "butanal", "condensed": "CH3CH2CH2CHO", "category": "Aldehyde & Ketone", "difficulty": "Medium"},
    {"smiles": "CC(C)C=O", "name": "2-methylpropanal", "condensed": "CH3CH(CH3)CHO", "category": "Aldehyde & Ketone", "difficulty": "Medium"},
    {"smiles": "CCCCC=O", "name": "pentanal", "condensed": "CH3CH2CH2CH2CHO", "category": "Aldehyde & Ketone", "difficulty": "Hard"},
    {"smiles": "CC(C)CC=O", "name": "3-methylbutanal", "condensed": "CH3CH(CH3)CH2CHO", "category": "Aldehyde & Ketone", "difficulty": "Hard"},
    {"smiles": "CCC(C)C=O", "name": "2-methylbutanal", "condensed": "CH3CH2CH(CH3)CHO", "category": "Aldehyde & Ketone", "difficulty": "Hard"},
    {"smiles": "CC(=O)C", "name": "propanone", "condensed": "CH3COCH3", "category": "Aldehyde & Ketone", "difficulty": "Easy", "alternative_names": ["acetone"]},
    {"smiles": "CCC(=O)C", "name": "butanone", "condensed": "CH3COCH2CH3", "category": "Aldehyde & Ketone", "difficulty": "Easy"},
    {"smiles": "CCCC(=O)C", "name": "pentan-2-one", "condensed": "CH3COCH2CH2CH3", "category": "Aldehyde & Ketone", "difficulty": "Medium"},
    {"smiles": "CCC(=O)CC", "name": "pentan-3-one", "condensed": "CH3CH2COCH2CH3", "category": "Aldehyde & Ketone", "difficulty": "Medium"},
    {"smiles": "CCCCC(=O)C", "name": "hexan-2-one", "condensed": "CH3COCH2CH2CH2CH3", "category": "Aldehyde & Ketone", "difficulty": "Hard"},
    {"smiles": "CCCC(=O)CC", "name": "hexan-3-one", "condensed": "CH3CH2COCH2CH2CH3", "category": "Aldehyde & Ketone", "difficulty": "Hard"},
    {"smiles": "CC(C)C(=O)C", "name": "3-methylbutan-2-one", "condensed": "CH3COCH(CH3)CH3", "category": "Aldehyde & Ketone", "difficulty": "Hard"},
    {"smiles": "CC(C)CC(=O)C", "name": "4-methylpentan-2-one", "condensed": "CH3COCH2CH(CH3)CH3", "category": "Aldehyde & Ketone", "difficulty": "Hard"},

    # === Primary Amine ===
    {"smiles": "CN", "name": "methanamine", "condensed": "CH3NH2", "category": "Primary Amine", "difficulty": "Easy", "alternative_names": ["methylamine"]},
    {"smiles": "CCN", "name": "ethanamine", "condensed": "CH3CH2NH2", "category": "Primary Amine", "difficulty": "Easy", "alternative_names": ["ethylamine"]},
    {"smiles": "CCCN", "name": "propan-1-amine", "condensed": "CH3CH2CH2NH2", "category": "Primary Amine", "difficulty": "Medium"},
    {"smiles": "CC(N)C", "name": "propan-2-amine", "condensed": "CH3CH(NH2)CH3", "category": "Primary Amine", "difficulty": "Medium"},
    {"smiles": "CCCCN", "name": "butan-1-amine", "condensed": "CH3CH2CH2CH2NH2", "category": "Primary Amine", "difficulty": "Medium"},
    {"smiles": "CCC(N)C", "name": "butan-2-amine", "condensed": "CH3CH(NH2)CH2CH3", "category": "Primary Amine", "difficulty": "Hard"},
    {"smiles": "CC(C)CN", "name": "2-methylpropan-1-amine", "condensed": "CH3CH(CH3)CH2NH2", "category": "Primary Amine", "difficulty": "Hard"},
    {"smiles": "CC(C)(C)N", "name": "2-methylpropan-2-amine", "condensed": "CH3C(CH3)(NH2)CH3", "category": "Primary Amine", "difficulty": "Hard", "alternative_names": ["tert-butylamine"]},

    # === Unsubstituted Amide ===
    {"smiles": "NC=O", "name": "methanamide", "condensed": "HCONH2", "category": "Unsubstituted Amide", "difficulty": "Easy", "alternative_names": ["formamide"]},
    {"smiles": "CC(=O)N", "name": "ethanamide", "condensed": "CH3CONH2", "category": "Unsubstituted Amide", "difficulty": "Easy", "alternative_names": ["acetamide"]},
    {"smiles": "CCC(=O)N", "name": "propanamide", "condensed": "CH3CH2CONH2", "category": "Unsubstituted Amide", "difficulty": "Medium"},
    {"smiles": "CCCC(=O)N", "name": "butanamide", "condensed": "CH3CH2CH2CONH2", "category": "Unsubstituted Amide", "difficulty": "Medium"},
    {"smiles": "CCCCC(=O)N", "name": "pentanamide", "condensed": "CH3CH2CH2CH2CONH2", "category": "Unsubstituted Amide", "difficulty": "Hard"},
    {"smiles": "CC(C)C(=O)N", "name": "2-methylpropanamide", "condensed": "CH3CH(CH3)CONH2", "category": "Unsubstituted Amide", "difficulty": "Hard"},
    {"smiles": "CC(C)CC(=O)N", "name": "3-methylbutanamide", "condensed": "CH3CH(CH3)CH2CONH2", "category": "Unsubstituted Amide", "difficulty": "Hard"},

    # === Ester ===
    {"smiles": "COC=O", "name": "methyl methanoate", "condensed": "HCOOCH3", "category": "Ester", "difficulty": "Easy", "alternative_names": ["methyl formate"]},
    {"smiles": "CC(=O)OC", "name": "methyl ethanoate", "condensed": "CH3COOCH3", "category": "Ester", "difficulty": "Easy", "alternative_names": ["methyl acetate"]},
    {"smiles": "CCOC=O", "name": "ethyl methanoate", "condensed": "HCOOCH2CH3", "category": "Ester", "difficulty": "Medium", "alternative_names": ["ethyl formate"]},
    {"smiles": "CC(=O)OCC", "name": "ethyl ethanoate", "condensed": "CH3COOCH2CH3", "category": "Ester", "difficulty": "Medium", "alternative_names": ["ethyl acetate"]},
    {"smiles": "CCC(=O)OC", "name": "methyl propanoate", "condensed": "CH3CH2COOCH3", "category": "Ester", "difficulty": "Medium"},
    {"smiles": "CCC(=O)OCC", "name": "ethyl propanoate", "condensed": "CH3CH2COOCH2CH3", "category": "Ester", "difficulty": "Hard"},
    {"smiles": "CC(=O)OCCC", "name": "propyl ethanoate", "condensed": "CH3COOCH2CH2CH3", "category": "Ester", "difficulty": "Hard"},
    {"smiles": "CCCC(=O)OC", "name": "methyl butanoate", "condensed": "CH3CH2CH2COOCH3", "category": "Ester", "difficulty": "Hard"}
]