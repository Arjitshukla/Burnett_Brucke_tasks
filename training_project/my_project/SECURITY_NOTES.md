# Login Protection — Limitations and Production Improvements

## Current Implementation

The Student Portal tracks failed login attempts using the UserProfile model.

- Login is temporarily blocked after 5 failed attempts.
- Account remains locked for 15 minutes.
- Login success, failure, account lock and blocked login events are stored in the AuditLog database table.
- Administrators can view audit records through Django Admin.

## Limitations

1. Failed attempts are tracked per username, not per IP address.
2. Audit logs currently store basic event information only.
3. The current implementation is suitable for a training project, not a complete production security system.
4. Database-based tracking may need additional concurrency protection when multiple login requests happen simultaneously.

## Production Improvements

1. Use Redis or a distributed cache for scalable login-attempt tracking.
2. Implement IP-based and username-based rate limiting.
3. Store additional security information, such as IP address and user agent, where appropriate.
4. Use centralized logging and monitoring tools.
5. Generate security alerts for suspicious login activities.
6. Protect audit logs against unauthorized modification and deletion.
7. Apply log retention policies to protect user privacy and manage storage.

## Conclusion

The current implementation provides basic login protection and audit tracking. A production system would require stronger rate limiting, centralized monitoring, secure log storage and additional security controls.