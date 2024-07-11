<h2>Setup the PostgreSql Database</h2>
<h4>1.Download the PGAdmin4 for the postgresql database</h4>
<h4>2.Create the server using right click on server and click register - server  </h4>
<h4>3.In Server In General tab add the name and in connection tab add new localhost name and new password</h4>
<h4>4.Create the database in the PGadmin4 using right click on postgre and create the database</h4>
<h4>5.In app.py code in app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/imgdb' instead of created newusername and newpassword</h4>
<h4>6.Run the app.py code and then open the Postman in post request run the localhost and then upload the image hit the sent button</h4>
<h4>7.The image has been uploaded</h4>
<h4>8.In Pgadmin4 in the created database select the query tool and the enter the Select * from upload</h4>
<h4>9.The image database has been created</h4>
