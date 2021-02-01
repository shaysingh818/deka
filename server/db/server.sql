CREATE TABLE IF NOT EXISTS accounts (
	account_id INTEGER PRIMARY KEY,
	service TEXT  NOT NULL UNIQUE, 
	username TEXT NOT NULL,
	password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS account_security_questions (
	question_id INTEGER, 
	question TEXT, 
	answer TEXT,
	question_account INTEGER, 
	FOREIGN KEY(question_account) REFERENCES accounts(account_id)
); 

CREATE TABLE IF NOT EXISTS decrypt_logs (
	log_id INTEGER, 
	ip_address TEXT, 
	user_agent TEXT,
	mac_address TEXT 
); 
