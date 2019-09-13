import argparse
import subprocess
import time
parser = argparse.ArgumentParser(description="Generate self signed-certificate")
#Create the certificate directory
testbed_cert_dir = "/Users/vignan/Documents/testbed/certs"
create_cert_dir = subprocess.run("mkdir vignan4",cwd=testbed_cert_dir,shell=True,capture_output=True,text=True)
#print (create_cert_dir.returncode)

verify_cert_dir = subprocess.run("ls", cwd = testbed_cert_dir,shell = True,capture_output= True,text = True)
#print (verify_cert_dir.stdout)
#print (verify_cert_dir.stderr)

if 'vignan4' in verify_cert_dir.stdout and create_cert_dir.returncode==0:
    create_cert_sub_working_dir = testbed_cert_dir+"/vignan4"
    #print (create_cert_sub_working_dir)
    create_cert_sub_directories = subprocess.run("mkdir certs crl newcerts private csr",
                                                 cwd = create_cert_sub_working_dir,
                                                 shell=True,capture_output=True, text=True)
    #print (create_cert_sub_directories.returncode)
    verify_cert_sub_directories = subprocess.run("ls", cwd = create_cert_sub_working_dir,
                                                 capture_output=True, text=True)
    #print verify_cert_sub_directories.returncode
    #print (verify_cert_sub_directories.stdout)

    create_index_file = subprocess.run("touch index.txt", cwd = create_cert_sub_working_dir, shell=True)
    start_cert_serial_num = subprocess.run("echo 1000 > serial", cwd = create_cert_sub_working_dir, shell=True)

    open_openssl_cnf_file = open('/Users/vignan/Documents/testbed/certs/openssl.cnf','r')
    new_openssl_cnf_file = open('/Users/vignan/Documents/testbed/certs/vignan4/openssl.cnf','w')
    for every_line in open_openssl_cnf_file.readlines():
        #print (every_line)
        if 'dir               =' in every_line:
            temp_var = every_line.split('=')
            #print (temp_var)
            temp_var[1] = create_cert_sub_working_dir
            #print (temp_var[1])
            #print (new_dir)
            new_openssl_cnf_file.write('dir               = ' + temp_var[1] + '\n')
        else:
            new_openssl_cnf_file.write(every_line)
    open_openssl_cnf_file.close()
    new_openssl_cnf_file.close()
    create_root_key_dir = "/Users/vignan/Documents/testbed/certs/vignan4/private/"
    create_root_key = subprocess.run('openssl genrsa -out ca.key.pem 4096',shell=True,
                                     cwd=create_root_key_dir)
    #print (create_root_key.stdout)
    #print (create_root_key.stderr)
    #print (create_root_key.returncode)
    time.sleep(10)
    create_root_certificate = subprocess.run('openssl req -config openssl.cnf -key private/ca.key.pem -new -x509 '
                                             '-days 7300 -sha256 -extensions v3_ca -out certs/ca.cert.pem '
                                             '-subj "/C=US/ST=NC/L=RTP/O=vignan4/OU=vignan4"',
                                             shell=True,cwd=create_cert_sub_working_dir)
    if create_root_certificate.returncode == 0:
        verify_root_certificate = subprocess.run('openssl x509 -noout -text -in certs/ca.cert.pem',shell=True,
                                                 cwd=create_cert_sub_working_dir,capture_output=True,text=True)
        print (verify_root_certificate.stdout)

