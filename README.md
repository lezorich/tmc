# Cumplo challenge

If not a valid key is provided, a 403 status code is returned.

Api key: 'SWvVO8RF.ZoqHc8jCYel6FIZPtqUiTieJ829fRAVn'
`Authorization: Api-Key ********`

`curl -X GET -H "Content-Type: application/json" -H "Authorization: Api-Key SWvVO8RF.ZoqHc8jCYel6FIZPtqUiTieJ829fRAVn" -d '{"credit_amount_uf": 1000, "credit_term_days": 366, "valid_at": "1/1/2020", "operation_type": "adjustable"}' http://localhost:8000/api/v1/tmc/`
