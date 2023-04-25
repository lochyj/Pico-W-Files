def get_credentials(file):
    creds = open(file, 'r');
    cred_lines = creds.read().replace('\r', '').split('\n');
    credentials = {};
    for line in cred_lines:
        if line.startswith('#'):
            continue;
        index = line.split(':');
        credentials.update(
            {index[0]:
                    (index[1].split('&')[0],
                     index[1].split('&')[1])}
        );
    return credentials;