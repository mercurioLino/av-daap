
import facebook as fb

graph = fb.GraphAPI('EAAJuk0ZAYiKwBADt3ZBv6CvC7hvioLNWmSJevCU3C1okUoZAs4rEJHnZBAWwwTvmyW3R8ZCtX8ZAqGktt5wKF4vwdo9Gd18NiebbZBDawjZAqBlrgfyTbEpMhipp3VZAlhfw2llTJpvFwJBbZB0ocE6ulQ8jU8YMhZB6o82kjR8YRLLaaRbiHcrM7qLgZBR2ENm3nwV90iZBR4OvGZAMFdG37CuZBgB')
app_id = '684528772876460' # Obtained from https://developers.facebook.com/
app_secret = '3c7530511daa730d13b039df31066d4f' # Obtained from https://developers.facebook.com/

# Extend the expiration time of a valid OAuth access token.
extended_token = graph.extend_access_token(app_id, app_secret)
print(extended_token)   
#verify that it expires in 60 days


# EAAJuk0ZAYiKwBAO9ZBO04rb1TscXfB6AEvRWE4omHPtXbM0dhsPMBZAPUCHBBZC4QEd4FyvggNWaeupTBPTFuoD6a0NJCjRkGbCuvKYi4n8KwHMLHFEkXS6MkvCugtcZCKasHQ3obZBQNMfJp6MDF3HPmmV1HVAZAswkJrm8rZAtaxl6bJTfzpKrbZBrl9zJ3tnIZD