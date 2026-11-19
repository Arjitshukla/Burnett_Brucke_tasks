# Django Session and Cookie Security

## Secure Cookie Settings

The following Django settings require HTTPS:

### 1. SESSION_COOKIE_SECURE
- When set to True, the session cookie is sent only over HTTPS connections.
- It protects session cookies from being transmitted over insecure HTTP connections.

### 2. CSRF_COOKIE_SECURE
- When set to True, the CSRF cookie is sent only over HTTPS connections.
- It helps protect CSRF tokens from being transmitted over insecure HTTP connections.

## Local HTTP Development

During local development using http://127.0.0.1:8000, these settings should generally remain False.

```python
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
```

If enabled blindly during HTTP development, the browser may not send these cookies, causing session or CSRF-related issues.

## Production Environment

When the application is deployed with HTTPS, enable both settings:

```python
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

## Other Session Settings

- SESSION_COOKIE_HTTPONLY: Prevents JavaScript from accessing the session cookie.
- SESSION_EXPIRE_AT_BROWSER_CLOSE: Controls whether the session expires when the browser closes.
- SESSION_COOKIE_AGE: Defines the session lifetime in seconds.

## Conclusion

Secure cookie settings should be enabled in production with HTTPS. They should not be blindly enabled during local HTTP development.