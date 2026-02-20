class DataAutomation:
    """
    Stores Plaid item and account data to the DB. Single responsibility; uses Connection (composition).
    plaid_item_id == represents a susccessful connection to a finaincal institution //not per account you have
    plaid_items_id_colum == holds the PK of the row created by your specific query in your session.
        //saves an extra query to db because insted of getting that most recent row you have that data already held in the felid
    """

    def __init__(self, connection):
        self._connection = connection


    def store_plaid_item_id(self, plaid_item_id):
        """Store plaid_item_id into plaid_items table. Returns the new row id (plaid_items_id_column)."""
        cur = self._connection.cursor()
        try:
            cur.execute(
                """
                INSERT INTO plaid_items (plaid_item_id, status)
                VALUES (%s, 'active')
                RETURNING id
                """,
                (plaid_item_id,),
            )
            plaid_items_id_column = cur.fetchone()[0]
            self._connection.get_connection().commit()
            return plaid_items_id_column
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store item_id: {str(e)}")
        finally:
            cur.close()

    def get_latest_plaid_item(self):
        """Return (plaid_items_id_column, access_token) for the most recent item with an access_token, or None, helps us retrive the item_id if n/a in memeory"""
        cur = self._connection.cursor()
        try:
            cur.execute(
                """
                SELECT id, access_token
                FROM plaid_items
                WHERE access_token IS NOT NULL
                ORDER BY id DESC
                LIMIT 1
                """,
            )
            row = cur.fetchone()
            return (row[0], row[1]) if row else None
        finally:
            cur.close()


    def store_access_token(self, access_token, plaid_items_id_column):
        """UPDATE access_token column FROM plaid_items table."""
        cur = self._connection.cursor()
        try:
            cur.execute(
                """
                UPDATE plaid_items
                SET access_token = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING id
                """,
                (access_token, plaid_items_id_column)
            )
            result = cur.fetchone()
            if result:
                self._connection.get_connection().commit()
                return result[0]
            else:
                raise Exception("No row found to update")
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store access_token: {str(e)}")
        finally:
            cur.close()


    def store_checking_accounts(self, checking_accounts, plaid_items_id_column):
        """INSERT into accounts table, Storing data for checking accounts //mask shows account to user without exposing account number"""
        cur = self._connection.cursor()
        try:
            for account in checking_accounts:
                cur.execute(
                    """
                    INSERT INTO accounts (
                        plaid_item_id, plaid_account_id, bank, name, mask, account_type,
                        current_balance, currency_code, status, last_synced_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    """,
                    (
                        plaid_items_id_column,
                        account.account_id,
                        getattr(account, "bank", None),
                        account.name,
                        getattr(account, "mask", None),
                        account.type.value if hasattr(account.type, "value") else str(account.type),
                        account.balances.current if account.balances else None,
                        account.balances.iso_currency_code if account.balances else "USD",
                        "open",
                    ),
                )
            self._connection.get_connection().commit()
            return len(checking_accounts)
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store checking accounts: {str(e)}")
        finally:
            cur.close()


    def store_credit_accounts(self, credit_accounts, plaid_items_id_column):
        """INSERT creditC accounts into accounts table."""
        cur = self._connection.cursor()
        try:
            for account in credit_accounts:
                cur.execute(
                    """
                    INSERT INTO accounts (
                        plaid_item_id, plaid_account_id, bank, name, mask, account_type,
                        balance_owed, credit_limit, currency_code, status, last_synced_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    """,
                    (
                        plaid_items_id_column,
                        account.account_id,
                        getattr(account, "bank", None),
                        account.name,
                        getattr(account, "mask", None),
                        account.type.value if hasattr(account.type, "value") else str(account.type),
                        account.balances.current if account.balances else None,
                        getattr(account.balances, "limit", None) if account.balances else None,
                        account.balances.iso_currency_code if account.balances else "USD",
                        "open",
                    ),
                )
            self._connection.get_connection().commit()
            return len(credit_accounts)
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store credit accounts: {str(e)}")
        finally:
            cur.close()


    def store_transactions(self, transactions, plaid_items_id_column):
        """INSERT into account_transactions (account_id, plaid_transaction_id, amount, date, transaction_time, merchant_name, category, status, iso_currency_code). transactions: list of dicts with plaid_account_id, plaid_transaction_id, date, amount, transaction_time, merchant_name, category, status, iso_currency_code. Resolves plaid_account_id to account_id. ON CONFLICT DO NOTHING. Returns number inserted."""
        if not transactions:
            return 0
        cur = self._connection.cursor()
        try:
            cur.execute("SELECT id, plaid_account_id FROM accounts WHERE plaid_item_id = %s", (plaid_items_id_column,))
            plaid_to_account_id = {row[1]: row[0] for row in cur.fetchall()}
            inserted = 0
            for t in transactions:
                account_id = plaid_to_account_id.get(t["plaid_account_id"])
                if account_id is None:
                    continue
                cur.execute(
                    """
                    INSERT INTO account_transactions (
                        account_id, plaid_transaction_id, amount, date, transaction_time,
                        merchant_name, category, status, iso_currency_code
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (account_id, plaid_transaction_id) DO NOTHING
                    """,
                    (
                        account_id,
                        t["plaid_transaction_id"],
                        t["amount"],
                        t["date"],
                        t.get("transaction_time"),
                        t.get("merchant_name"),
                        t.get("category"),
                        t.get("status", "posted"),
                        t.get("iso_currency_code") or "USD",
                    ),
                )
                if cur.rowcount:
                    inserted += 1
            self._connection.get_connection().commit()
            return inserted
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store transactions: {str(e)}")
        finally:
            cur.close()




"""
plaid_items_id_column:
we store the recent id incremrented count in the vairable plaid_items_id_column to save a hit to the db, this is benficial for performace and scalability
"""