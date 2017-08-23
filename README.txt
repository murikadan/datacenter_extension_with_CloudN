# Required python packages 
# 1. json
# 2. requests
# Handling of crdentials
#	ACX crdentials
#		store admin account username and passsword in 'acx_crdentials.txt' file
#		eg. file content
#		admin
#		password
#	License Id
#		store CloudN license id in 'license.txt' file
#		eg. file content
#		yasser-123456.01
#	AWS Credentials
#		store aws access key and secret key in 'aws_crdentials.txt' file
#		eg. file content
#		ABCDEFGHIJKL
#		ABC1233+-EFGHIJKLMNOPQRST
# SSL
#	Verification of SSL certificate is currently disabled due to common name mismatch.
#   (Initially there was problem with windows not trusting the certificate authrority, however that was mitigated by 
#	explicitly adding the cert to trusted certificates)
#	Install certificate with correct common name and re-enabe certificate verification