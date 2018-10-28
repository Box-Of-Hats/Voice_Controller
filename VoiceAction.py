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

    def __init__(self, match_patterns, function, about_text='', kwargs={}):
        self.match_patterns = match_patterns
        self.function = function
        self.about_text = about_text
        self.kwargs = kwargs

    def is_match(self, phrase):
        """
        Check if a given phrase matches the assosiated phrase for this action.
        >>> va = VoiceAction(["please google __search_phrase__ for me"], print)
        >>> va.is_match("please google a cool search phrase for me")
        'please google __search_phrase__ for me'

        >>> va.is_match("please google something cool")
        False

        >>> va = VoiceAction(["google __search_phrase__"], print)
        >>> va.is_match("google best memes 2018")
        'google __search_phrase__'

        """
        for match_pattern in self.match_patterns:
            phrase_args = re.findall("__[a-zA-Z0-9_]*__", match_pattern)
            match_pattern_without_args = match_pattern
            for pa in phrase_args:
                match_pattern_without_args = match_pattern_without_args.replace(
                    pa, "[ ,.a-zA-Z0-9]*")

            if re.match(match_pattern_without_args, phrase):
                return match_pattern
        return False

    def get_values(self, phrase, match_pattern):
        """
        Take a phrase and a given match pattern and extract the args with their values

        >>> va = VoiceAction(["google __search_phrase__"], print)
        >>> va.get_values("google pictures of cats", "google __search_phrase__")
        {'search_phrase': 'pictures of cats'}

        >>> va = VoiceAction(["search for __search_phrase__ on __search_engine__"], print)
        >>> va.get_values("search for pictures of cats on google", "search for __search_phrase__ on __search_engine__")
        {'search_phrase': 'pictures of cats', 'search_engine': 'google'}

        """
        phrase_args = re.findall("__[a-zA-Z0-9_]*__", match_pattern)
        for pa in phrase_args:
            match_pattern = match_pattern.replace(pa, "([ ,.a-zA-Z0-9]*)")

        match_pattern = re.compile(match_pattern)
        m = match_pattern.findall(phrase)

        # If there is more than 1 match found, we need to take the first nested tuple
        if isinstance(m[0], tuple):
            m = m[0]

        results = {}
        for no, pa in enumerate(phrase_args):
            pa = pa.strip("_")
            results[pa] = m[no]

        return results

    def execute(self, kwargs):
        # Combine given kwargs with any default kwargs defined for this action
        kwargs.update(self.kwargs)
        return self.function(**kwargs)


if __name__ == "__main__":
    doctest.testmod()
