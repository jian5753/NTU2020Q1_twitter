import re


class stopRule():
    def __init__(self, ruleType, rule):
        self.ruleType = ruleType
        self.rule = rule

    def shouldStop(self, word):
        if self.ruleType == 'lenLessThan':
            return len(word) <= int(self.rule)
        elif self.ruleType == 'regex':
            return re.match(self.rule, word)
