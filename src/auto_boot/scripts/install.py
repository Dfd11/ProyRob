import robot_upstart

j = robot_upstart.Job(name="proyrob_job")
j.symlink = True

j.add(package="proyrob",filename="launch/proyrob.launch")

j.install()
