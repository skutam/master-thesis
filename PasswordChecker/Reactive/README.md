# Reactive password checkers

There are 3 implementations of the reactive password checkers in `libs` directory, for each popular backend language.
Each implementation is a `Client-Server` application and uses the python server in directory `server` that is required
to be started before testing the client applications in `libs` directories.

The `credentials` dictionary contains `db.ini` file that contains the credentials for database, change them to
reflex the configuration that is used.