from checkin_api.app import create_app

if __name__ == '__main__':
    app = create_app(testing=True)
    app.run()
