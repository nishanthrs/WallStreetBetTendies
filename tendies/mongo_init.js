db.createUser(
    {
        user: "mongo",
        pwd: "411_wsb_tendies",
        roles: [
            {
                role: "readWrite",
                db: "wsb_tendies"
            }
        ]
    }
);

