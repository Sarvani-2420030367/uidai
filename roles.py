def filter_data_by_role(df, user):
    if user["role"] == "ADMIN":
        return df
    elif user["role"] == "STATE":
        return df[df["state"] == user["state"]]
    elif user["role"] == "DISTRICT":
        return df[
            (df["state"] == user["state"]) &
            (df["district"] == user["district"])
        ]
