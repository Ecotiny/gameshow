# Backend
Endpoints are:
 - `/api/score`:
   - GET: get score info
   - PUT: update score info (`{party: <partyname>, value: <new_amount>}`)
 - `/api/party`: get all domain names, field names, and subfield names
   - DELETE: delete party (`{party: <partyname>}`)
   - POST: add party (`{party: <partyname>}`)
