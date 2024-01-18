-- Assuming you have a table named 'user' with columns 'user_id', 'email', and 'valid_email'
-- This trigger will reset 'valid_email' to 0 when 'email' is updated

DELIMITER //
CREATE TRIGGER trg_reset_valid_email
BEFORE UPDATE ON user
FOR EACH ROW
BEGIN
    IF NEW.email != OLD.email THEN
        SET NEW.valid_email = 0;
    END IF;
END//
DELIMITER ;
