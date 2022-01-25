
import facebook as fb

# https://developers.facebook.com/tools/debug/accesstoken/

"""
Script que aumenta o tempo de duração do token de acesso a página. Por padrão esse token
dura apenas 2 horas, logo precisa ser extendido, obtendo assim um tempo de duração 
de 2 meses e evitando problemas de autenticação.
"""
graph = fb.GraphAPI('')
app_id = ''
app_secret = ''

# Extende o tempo de expiração do token
extended_token = graph.extend_access_token(app_id, app_secret)
print(extended_token)   
# EAAJuk0ZAYiKwBAO9ZBO04rb1TscXfB6AEvRWE4omHPtXbM0dhsPMBZAPUCHBBZC4QEd4FyvggNWaeupTBPTFuoD6a0NJCjRkGbCuvKYi4n8KwHMLHFEkXS6MkvCugtcZCKasHQ3obZBQNMfJp6MDF3HPmmV1HVAZAswkJrm8rZAtaxl6bJTfzpKrbZBrl9zJ3tnIZD