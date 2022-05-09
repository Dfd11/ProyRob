import robot_upstart
print("CREATE JOB")
j = robot_upstart.Job(name="proyrob_job")
j.symlink = True
print("ADD PACKAGE")
j.add(package="proyrob",filename="launch/proyrob.launch")
print("INSTALL")
j.install()
