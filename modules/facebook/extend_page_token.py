
import facebook as fb

graph = fb.GraphAPI('EAAJuk0ZAYiKwBAOReBPmZBGABLLrFzHDEqUvQSj1OAAUfn8vx1TTX3MaYmohVsHhwUjBxIKO8vdromZCWyP8J5QQGZBnhrvWYOzZAKwnPZA1TToPVconh6KBk9xepxIeuaBEkmxvHpIXPMU2EHKOcsYgpATuoZCWTh2defPTU4Xls2HWynrxJCrvIafsamFCpJv67kSYW99FswZAygygVCnA')
app_id = '684528772876460' # Obtained from https://developers.facebook.com/
app_secret = '3c7530511daa730d13b039df31066d4f' # Obtained from https://developers.facebook.com/

# Extend the expiration time of a valid OAuth access token.
extended_token = graph.extend_access_token(app_id, app_secret)
print(extended_token)   
#verify that it expires in 60 days

# https://developers.facebook.com/tools/debug/accesstoken/
# EAAJuk0ZAYiKwBAO9ZBO04rb1TscXfB6AEvRWE4omHPtXbM0dhsPMBZAPUCHBBZC4QEd4FyvggNWaeupTBPTFuoD6a0NJCjRkGbCuvKYi4n8KwHMLHFEkXS6MkvCugtcZCKasHQ3obZBQNMfJp6MDF3HPmmV1HVAZAswkJrm8rZAtaxl6bJTfzpKrbZBrl9zJ3tnIZD