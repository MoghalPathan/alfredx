from difflib import SequenceMatcher
import re

class WinterSoldierProtocol:
    """Winter Soldier with 50+ variations per word"""
    
    TRIGGER_WORDS = [
        "longing", "rusted", "seventeen", "daybreak", 
        "furnace", "nine", "benign", "homecoming", 
        "one", "freight car"
    ]
    
    # 50+ variations per word
    VARIATIONS = {
        "longing": [
            "long", "longin", "longing", "belonging", "lunging", "logging", "lounging",
            "longings", "lung", "lounge", "lunge", "langing", "longen", "longeing",
            "longging", "longue", "languid", "longish", "longhand", "longitude",
            "lawnging", "loungin", "loanging", "lawning", "lungeing", "lawnin",
            "longview", "longterm", "loin", "longa", "longue", "longer", "longest",
            "longan", "longboat", "longbow", "longcase", "longe", "longeron",
            "longevity", "longface", "longfin", "longform", "longhair", "longhand",
            "longhaul", "longhead", "longhorn", "longhouse", "longicorn", "longing's"
        ],
        
        "rusted": [
            "rust", "rusted", "trusted", "rushed", "roasted", "roosted", "rested",
            "rustad", "rusteed", "rusten", "rustin", "rustid", "rustud", "rusty",
            "ruste", "rustled", "rastid", "restid", "rosted", "rustad", "rustad",
            "russed", "rustard", "rustum", "rustup", "rustik", "rustic", "rustical",
            "rustier", "rustiest", "rustily", "rustiness", "rusting", "rustless",
            "rustproof", "rusts", "russet", "russian", "rustburg", "rustler",
            "rustling", "trustid", "trustad", "rustedt", "roasted", "busted",
            "dusted", "gusted", "justed", "lusted", "musted", "wusted"
        ],
        
        "seventeen": [
            "17", "seven teen", "seventeeen", "seventin", "seventein", "seventine",
            "seventen", "seventyn", "sevinteen", "sevenTeen", "7teen", "7-teen",
            "seventeen's", "seventeens", "seventeenish", "seventeener", "seventeeners",
            "sventeen", "secenteen", "seventaan", "seventien", "seventijn", "seventyn",
            "sebinteen", "sebeenteen", "seventean", "seventeam", "seventeens",
            "sebenteen", "seventeent", "seventeente", "seventeented", "seventeently",
            "seventeenthly", "seventeenths", "sevintin", "sivteen", "siventen",
            "sibinteen", "saventeen", "sevinteeen", "seventween", "seventean",
            "seventine", "sevantean", "sevantien", "savantean", "suventeen", "suvinteen"
        ],
        
        "daybreak": [
            "dawn", "day break", "day-break", "date break", "daybrake", "daybreack",
            "daybrak", "deybreak", "day breck", "daybreck", "daibreak", "day-breck",
            "day brake", "die break", "daybreaking", "daybreaks", "day's break",
            "dey break", "dei break", "daibrake", "daibrak", "daybreaker", "daybreakers",
            "daybreakish", "deybrake", "deybreck", "die brake", "die breck",
            "diebreak", "datebreak", "databreak", "dayberak", "day berak", "day-berak",
            "daybrick", "day brick", "daibrick", "dey brick", "dei brick",
            "daybrook", "day brook", "deybrook", "deibrook", "dai brook",
            "day's dawn", "daylit", "daylight", "daylighting", "dayburst", "day burst"
        ],
        
        "furnace": [
            "furnish", "furnace", "furniss", "furnace's", "furnaces", "furnice",
            "furnise", "furnas", "furnase", "furnis", "furnace", "furnas",
            "fornace", "forniss", "fornish", "furnesce", "furnish", "furnace's",
            "furnacelike", "furnaceman", "furnacemen", "furnaceward", "furnishing",
            "furnisher", "furnaced", "furnacing", "furnaceroom", "furnas", "furnesse",
            "furniss", "furniess", "furniss", "furnesse", "furnish", "furnishings",
            "furniture", "furnacer", "furnacers", "furnacework", "furnaceworker",
            "fernace", "ferniss", "fernish", "ferness", "fernis", "fornace",
            "fornas", "forniss", "fornesh", "fornish", "fernice", "furnase"
        ],
        
        "nine": [
            "mine", "9", "nein", "night", "nines", "nine's", "ninee", "nyne",
            "niine", "nien", "nyne", "nain", "nien", "nin", "nyne", "nein",
            "neun", "negen", "naoi", "nau", "nina", "niner", "niners",
            "ninefold", "ninepence", "ninepenny", "ninepin", "ninepins", "ninescore",
            "nineteen", "ninety", "ninth", "ninths", "ninthly", "nining",
            "ninely", "ninish", "nineish", "ninesome", "ninewise", "nein's",
            "nine-sided", "nine-fold", "mine", "fine", "line", "pine", "vine",
            "wine", "dine", "sign", "shine", "shrine", "define", "design"
        ],
        
        "benign": [
            "bening", "begin", "being", "benign", "benigns", "benign's", "benigne",
            "benigno", "benin", "benine", "benight", "benighted", "benignant",
            "benignantly", "benignity", "benignities", "benignly", "benignness",
            "beniign", "beneign", "beniegn", "beningn", "bennign", "beniggn",
            "beneggn", "beneing", "bengine", "bening", "beneign", "benight",
            "bennign", "bengn", "benin", "beningne", "beniing", "beneening",
            "beginning", "begins", "begun", "began", "being", "beings",
            "bein", "bean", "been", "beaning", "beeing", "beaning",
            "begine", "begining", "beginnin", "begginning", "beggining", "begginin"
        ],
        
        "homecoming": [
            "home coming", "home-coming", "homing", "homecomming", "homecomeing",
            "homecomins", "homecoming's", "homecomings", "home's coming",
            "homecommin", "homecomin", "homecomen", "homecommings", "homecommins",
            "homcomeing", "homcomen", "homcoming", "hom coming", "hom-coming",
            "homecomeing", "homecommeing", "homecoamen", "hoamcoming", "hoamcomming",
            "homecumming", "homecooming", "homecombing", "home-combing", "homecommbing",
            "homecomink", "homecomink", "homcoming", "homicoming", "homicomming",
            "hamecoming", "hamecomming", "homecomers", "homecomingness", "homecomer",
            "homecomeless", "homecominglike", "home coming's", "homecommers",
            "homecommen", "homecommens", "homecoamed", "homecoamen", "hoamcomen",
            "coming home", "coming-home", "cominghome", "comminghome", "comminhome"
        ],
        
        "one": [
            "won", "1", "wan", "on", "own", "oan", "onn", "one's", "ones",
            "onee", "wone", "wun", "whone", "onne", "onee", "un", "une",
            "aan", "een", "ane", "onne", "onea", "onei", "oney", "onea",
            "oneh", "onew", "oner", "onet", "onef", "oneg", "oneb", "onem",
            "onez", "onec", "oned", "onep", "onel", "onev", "onek", "oneq",
            "onex", "onez", "anone", "anyone", "everyone", "someone", "only",
            "once", "oncer", "onced", "oncing", "oneness", "onefold", "oneself"
        ],
        
        "freight car": [
            "freightcar", "freight-car", "freight", "train car", "freight train",
            "fright car", "frate car", "fraight car", "freit car", "frieght car",
            "freigt car", "freightcars", "freight-cars", "freight cars", "freightkar",
            "freight kar", "fraight-car", "freit-car", "frieght-car", "freigt-car",
            "freightcaar", "freight caar", "freightcart", "freight cart", "freightcart",
            "fraightcar", "fraitcar", "freitcar", "frightcar", "freight wagon",
            "freight-wagon", "freightwagon", "cargo car", "cargo-car", "cargocar",
            "train freight", "traincar", "train-car", "freight vehicle", "freight-vehicle",
            "freightvehicle", "fraitkar", "freitkar", "frightkar", "freightker",
            "freight ker", "fraight ker", "freit ker", "frieght ker", "freigt ker",
            "freightcarre", "freight carre", "freightcarr", "freight carr", "frecar",
            "fre car", "freight carrier", "freight-carrier", "freightcarrier"
        ]
    }
    
    def __init__(self):
        self.current_index = 0
        self.attempts = 0
        self.max_attempts = 7  # More attempts with more variations
        
    def check_word(self, spoken_word):
        """Enhanced matching with 50+ variations"""
        spoken_word = spoken_word.lower().strip()
        spoken_word = re.sub(r'[^\w\s]', '', spoken_word)  # Remove punctuation
        
        expected = self.TRIGGER_WORDS[self.current_index]
        
        # 1. Exact match
        if spoken_word == expected:
            return self._advance()
            
        # 2. Check all 50+ variations
        if expected in self.VARIATIONS:
            for variant in self.VARIATIONS[expected]:
                # Exact variant match
                if spoken_word == variant:
                    return self._advance()
                # Variant contained in spoken
                if variant in spoken_word and len(variant) >= 3:
                    return self._advance()
                # Spoken contained in variant
                if spoken_word in variant and len(spoken_word) >= 3:
                    return self._advance()
                    
        # 3. Fuzzy match (60% similarity for flexibility)
        similarity = SequenceMatcher(None, spoken_word, expected).ratio()
        if similarity >= 0.60:
            return self._advance()
            
        # 4. Substring match
        if len(spoken_word) >= 4:
            if expected in spoken_word or spoken_word in expected:
                return self._advance()
        
        # Failed - show hints
        self.attempts += 1
        if self.attempts >= self.max_attempts:
            self.reset()
            return {
                "status": "failed",
                "message": f"Reset. Word was: {expected.upper()}"
            }
            
        # Random 5 hints from variations
        hints = self.VARIATIONS.get(expected, [expected])[:5]
        return {
            "status": "retry",
            "expected": expected,
            "hints": hints,
            "attempts_left": self.max_attempts - self.attempts,
            "progress": self.current_index,
            "total": len(self.TRIGGER_WORDS),
            "message": f"Try: {expected.upper()} (or: {', '.join(hints[:3])})"
        }
        
    def _advance(self):
        """Advance to next word"""
        self.current_index += 1
        self.attempts = 0
        
        if self.current_index >= len(self.TRIGGER_WORDS):
            self.reset()
            return {
                "status": "activated",
                "message": "⚡⚡⚡ SOLDIER READY FOR COMPLIANCE ⚡⚡⚡"
            }
            
        return {
            "status": "continue",
            "next_word": self.TRIGGER_WORDS[self.current_index],
            "progress": self.current_index,
            "total": len(self.TRIGGER_WORDS)
        }
        
    def reset(self):
        self.current_index = 0
        self.attempts = 0
        
    def get_status(self):
        hints = self.VARIATIONS.get(self.TRIGGER_WORDS[self.current_index], [])[:5]
        return {
            "current_word": self.TRIGGER_WORDS[self.current_index],
            "progress": self.current_index,
            "total": len(self.TRIGGER_WORDS),
            "hints": hints
        }
