== Files ==

* db.sql - script for creating tables in database. Please be carefully because this script drop
          already existing tables in database. (It works only for mysql database because has been 
          create by 'mysqldump' program ).

* aligner-apache.conf - configuration file for apache  which display catalogues in file system 
                       into the URLs on site.

== Directories ==

* clear_php/etc - actual for php scripts configuration.

* clear_php/system - php library to organize site.     

* clear_php/site  - set of php scripts, which organize site structure.


If you interesting in installation this web interface on  website please create tables
in database and copy (may be with modifications) file aligner-apache.conf into the 
/etc/apache2/conf.d directory or like. It is possible create this records in the 
certain virtual hosts.

This site uses SSL for user authorization, so please enable SSL on your site. 



