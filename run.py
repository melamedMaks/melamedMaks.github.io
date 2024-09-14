from markupsafe import Markup
from app.routes.routes import app

def format_currency(value):
    return Markup('${:,.0f}'.format(value))

app.jinja_env.filters['to_currency'] = format_currency

if __name__ == '__main__':
    app.run(debug=True)