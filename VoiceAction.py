import re
import doctest

class VoiceAction():
    """
    Object to hold a mapping of a voice phrase and a function.
    Substitute argument positions in phrase with '__argument_name__'. These will be passed into
    the associated function as named arguments.
    Example
        matched_patterns = [
            "search google for __search_phrase__",
            "google __search_phrase__",
            "search for __search_phrase__ on google"
        ]
        'search google for pictures of cats'
        will call google_search("pictures of cats")
    """
    def __init__(self, match_patterns, function, arg_pos=-1, about_text=''):
        self.match_patterns = match_patterns
        self.function = function
        self.arg_pos = arg_pos
        self.about_text = about_text

    def is_match(self, phrase, ):
        """
        Check if a given phrase matches the assosiated phrase for this action.
        >>> va = VoiceAction(["please google __search_phrase__ for me"], print)
        >>> va.is_match("please google a cool search phrase for me")
        True

        >>> va = VoiceAction(["google __search_phrase__"], print)
        >>> va.is_match("google best memes 2018")
        True
        
        >>> va = VoiceAction(["please google __search_phrase__ for me"], print)
        >>> va.is_match("please google something cool")
        False

        """
        for match_pattern in self.match_patterns:
            phrase_args = re.findall("__[a-zA-Z0-9_]*__", match_pattern)
            for pa in phrase_args:
                match_pattern = match_pattern.replace(pa, "[ ,.a-zA-Z0-9]*")
                
            if re.match(match_pattern, phrase):
                return True
        return False

    def execute(self):
        pass

if __name__ == "__main__":
    doctest.testmod()