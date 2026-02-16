class DataAutomation:
    """Stores Plaid item and account data to the DB. Single responsibility; uses Connection (composition)."""

    def __init__(self, connection):
        self._connection = connection


    def store_link_token(self, link_token):
        """Store link token. Note: Link tokens are temporary and typically not stored in DB."""
        # Note: plaid_items table doesn't have a link_token column
        # This method is provided per request but link tokens are single-use and expire
        cur = self._connection.cursor()
        try:
            # If you add a link_token column to plaid_items, uncomment below:
            # cur.execute(
            #     """
            #     INSERT INTO plaid_items (link_token, status)
            #     VALUES (%s, 'pending')
            #     RETURNING id
            #     """,
            #     (link_token,)
            # )
            # item_db_id = cur.fetchone()[0]
            # self._connection.get_connection().commit()
            # return item_db_id
            pass  # Link tokens are not stored - they're temporary
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store link token: {str(e)}")
        finally:
            cur.close()

    def store_item_id(self, plaid_item_id):
        """Store Plaid item_id into plaid_items table."""
        cur = self._connection.cursor()
        try:
            cur.execute(
                """
                INSERT INTO plaid_items (plaid_item_id, status)
                VALUES (%s, 'active')
                RETURNING id
                """,
                (plaid_item_id,)
            )
            item_db_id = cur.fetchone()[0]
            self._connection.get_connection().commit()
            return item_db_id
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store item_id: {str(e)}")
        finally:
            cur.close()

    def store_access_token(self, access_token, plaid_item_db_id):
        """Update access_token for an existing plaid_items row."""
        cur = self._connection.cursor()
        try:
            cur.execute(
                """
                UPDATE plaid_items
                SET access_token = %s, updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
                RETURNING id
                """,
                (access_token, plaid_item_db_id)
            )
            result = cur.fetchone()
            if result:
                item_db_id = result[0]
            else:
                raise Exception("No row found to update")
            self._connection.get_connection().commit()
            return item_db_id
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store access_token: {str(e)}")
        finally:
            cur.close()

    def store_plaid_item(self, plaid_item_id, access_token):
        """INSERT into plaid_items with both item_id and access_token. Returns the DB id for linking accounts."""
        cur = self._connection.cursor()
        try:
            cur.execute(
                """
                INSERT INTO plaid_items (plaid_item_id, access_token, status)
                VALUES (%s, %s, 'active')
                RETURNING id
                """,
                (plaid_item_id, access_token)
            )
            item_db_id = cur.fetchone()[0]
            self._connection.get_connection().commit()
            return item_db_id
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store Plaid item: {str(e)}")
        finally:
            cur.close()


    def store_accounts(self, accounts, plaid_item_db_id):
        """INSERT each account into accounts. plaid_item_db_id is the FK to plaid_items.id."""
        cur = self._connection.cursor()
        try:
            for account in accounts:
                cur.execute(
                    """
                    INSERT INTO accounts (
                        plaid_item_id, plaid_account_id, name, mask, account_type,
                        current_balance, balance_owed, credit_limit, currency_code, status, last_synced_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                    """,
                    (
                        plaid_item_db_id,
                        account.account_id,
                        account.name,
                        getattr(account, "mask", None),
                        account.type.value if hasattr(account.type, "value") else str(account.type),
                        account.balances.current if account.balances else None,
                        account.balances.current if (account.balances and str(account.type).lower() == "credit") else None,
                        getattr(account.balances, "limit", None) if account.balances else None,
                        account.balances.iso_currency_code if account.balances else "USD",
                        "open",
                    ),
                )
            self._connection.get_connection().commit()
            return len(accounts)
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store accounts: {str(e)}")
        finally:
            cur.close()
