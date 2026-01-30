def setup_toolbar(self):
        toolbar = QToolBar("Django Controls")
        toolbar.setIconSize(QSize(20, 20))
        toolbar.setMovable(False)
        toolbar.setStyleSheet("QToolBar { background-color: #333333; border-bottom: 1px solid #444; spacing: 10px; padding: 5px; }")
        self.addToolBar(toolbar)

        def add_action(name, icon_type, method):
            icon = self.style().standardIcon(icon_type)
            action = QAction(icon, name, self)
            action.triggered.connect(method)
            toolbar.addAction(action)
            return action

        # Server Group
        toolbar.addWidget(QLabel(" SERVER:"))
        self.act_run = add_action("Run Server", QStyle.SP_MediaPlay, self.run_dev_server)
        self.act_stop = add_action("Stop Server", QStyle.SP_MediaStop, self.stop_dev_server)
        self.act_stop.setEnabled(False)
        
        toolbar.addSeparator()

        # Database Group
        toolbar.addWidget(QLabel(" DB: "))
        add_action("Make Migrations", QStyle.SP_FileIcon, self.make_migrations)
        add_action("Migrate", QStyle.SP_DialogApplyButton, self.run_migrate)

        toolbar.addSeparator()

        # Utils
        toolbar.addWidget(QLabel(" UTILS: "))
        add_action("New App", QStyle.SP_FileDialogNewFolder, self.open_new_app_dialog)
