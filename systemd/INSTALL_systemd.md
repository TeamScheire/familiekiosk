Use systemd to autostart the familykiosk

The given systemd services must be stored in

    /lib/systemd/system/

so do:

    sudo cp fk_mariabot.service /lib/systemd/system/
    sudo cp fk_tvbox.service /lib/systemd/system/

and set the correct permissions (644)

    sudo chmod 644 /lib/systemd/system/fk_mariabot.service
    sudo chmod 644 /lib/systemd/system/fk_tvbox.service

Now make sure the service starts:

    sudo systemctl daemon-reload
    sudo systemctl enable fk_mariabot.service
    sudo systemctl enable fk_tvbox.service
