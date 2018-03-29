curl -o latest.dump `heroku pg:backups public-url -a politicalsisterhood-production` \
&& dropdb political_sisterhood \
&& createdb political_sisterhood \
&& pg_restore --verbose --clean --no-acl --no-owner -h localhost -d political_sisterhood latest.dump \
&& rm latest.dump
