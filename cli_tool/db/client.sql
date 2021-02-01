
CREATE TABLE IF NOT EXISTS account_keys (
	id integer PRIMARY KEY,
	service text NOT NULL, 
	key text NOT NULL 
);


CREATE TABLE IF NOT EXISTS question_keys (
	question_id INTEGER, 
	question TEXT, 
	key TEXT, 
	question_account INTEGER, 
	FOREIGN KEY(question_account) REFERENCES accounts(id)
); 

