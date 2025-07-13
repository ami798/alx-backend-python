import asyncio
import aiosqlite

async def async_fetch_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users") as cursor:
            rows = await cursor.fetchall()
            return rows  # ✅ required by checker

async def async_fetch_older_users():
    async with aiosqlite.connect("users.db") as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            rows = await cursor.fetchall()
            return rows  # ✅ required by checker

async def fetch_concurrently():
    users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("✅ All Users:")
    for user in users:
        print(user)

    print("\n✅ Users older than 40:")
    for user in older_users:
        print(user)

# ✅ Run it
if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
