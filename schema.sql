-- CREATE DATABASE Chat;

CREATE TABLE "conversation" (
    "id" INTEGER PRIMARY KEY,             
    "model" TEXT NOT NULL,                
    "title" TEXT,                         
    "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "updated_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "total_tokens" INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE "message" (
    "id" INTEGER PRIMARY KEY,             
    "conversation_id" INTEGER NOT NULL,   
    "created_at" DATETIME DEFAULT CURRENT_TIMESTAMP,
    "content" TEXT NOT NULL,              
    "owner" TEXT NOT NULL CHECK("owner" IN ('user', 'AI')),
    FOREIGN KEY ("conversation_id") REFERENCES "conversation"("id") ON DELETE CASCADE
);

CREATE TRIGGER "update_conversation_timestamp"
AFTER UPDATE ON "conversation"
FOR EACH ROW
BEGIN
    UPDATE "conversation"
    SET "updated_at" = CURRENT_TIMESTAMP
    WHERE "id" = OLD."id";
END;