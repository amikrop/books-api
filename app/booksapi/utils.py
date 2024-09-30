def get_user_display(user):
    display = f"<{user.email}>"

    full_name = user.get_full_name()
    if full_name:
        display = f"{full_name} {display}"

    return display
