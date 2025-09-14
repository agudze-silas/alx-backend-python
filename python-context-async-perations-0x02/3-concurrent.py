import asyncio
import aiosqlite


async def async_fetch_users(db_name="test.db"):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users") as cursor:
            return await cursor.fetchall()


async def async_fetch_older_users(db_name="test.db"):
    async with aiosqlite.connect(db_name) as db:
        async with db.execute("SELECT * FROM users WHERE age > 40") as cursor:
            return await cursor.fetchall()


async def fetch_concurrently():
    # Run both queries at the same time
    results_all, results_older = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )

    print("All Users:")
    for row in results_all:
        print(row)

    print("\nUsers Older than 40:")
    for row in results_older:
        print(row)


if __name__ == "__main__":
    asyncio.run(fetch_concurrently())
    
