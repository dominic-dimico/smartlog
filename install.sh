#~/bin/bash


source "./smartlog.sh"

who=`whoami`
if [ "$who" != "root" ]
then
	die "You must be root to run the installer"
fi


if ! check_dir "smartlog lib" "$HOME/.sh"
then
	s_ex "Making smartlog library directory" "mkdir -p $HOME/.sh"
  cp smartlog.sh $HOME/.sh/
fi

if ! check_dir "smartlog log" "$HOME/.smartlog"
then
	s_ex "Making smartlog log directory" "mkdir -p $HOME/.sh"
fi
cp smartlog.sh $HOME/.sh/


#versions=`ls /usr/lib*/python* -d`
#for version in `ls $versions -d`
#do
#	s_ex "Deleting old folder in $version" "rm -rf $version/site-packages/smartlog"
#	s_ex "Creating folder in $version" "mkdir $version/site-packages/smartlog"
#	s_ex "Installing in $version"      "cp smartlog.py $version/site-packages/smartlog/__init__.py"
#done
