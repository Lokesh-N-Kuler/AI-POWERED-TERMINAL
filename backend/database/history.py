from database.database import get_connection


def save_command(
    command,
    shell,
    cwd,
    stdout,
    stderr,
    exit_code,
):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO command_history
        (command, shell, cwd, stdout, stderr, exit_code)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (
            command,
            shell,
            cwd,
            stdout,
            stderr,
            exit_code,
        ),
    )

    connection.commit()
    connection.close()


def get_history(limit=100):
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT *
        FROM command_history
        ORDER BY id DESC
        LIMIT ?
        """,
        (limit,),
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def clear_history():
    connection = get_connection()

    connection.execute("DELETE FROM command_history")

    connection.commit()
    connection.close()