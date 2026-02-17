class DataAutomation:
    """Stores Plaid item and account data to the DB. Single responsibility; uses Connection (composition)."""

    def __init__(self, connection):
        self._connection = connection


    def store_plaid_item_id(self, plaid_item_id):
        """Store plaid_item_id into plaid_items table, Plaid has its own identifier for every account connected"""
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
            plaid_items_id_column = cur.fetchone()[0]
            self._connection.get_connection().commit()
            return plaid_items_id_column
        except Exception as e:
            self._connection.get_connection().rollback()
            raise Exception(f"Failed to store item_id: {str(e)}")
        finally:
            cur.close()
    

    def store_access_token(self, access_token, plaid_items_id_column):
        """UPDATE access_token column into plaid_items table."""
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


    def store_accounts(self, accounts, plaid_items_id_column):
        """INSERT each account into accounts. plaid_items_id_column is FK to plaid_items.id."""
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
                        plaid_items_id_column,
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
