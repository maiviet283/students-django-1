## Giới thiệu server web quản lý sinh viên

### 1. Sử dụng Django để xây dựng server web quản lý sinh viên
Django là một framework web mạnh mẽ và dễ sử dụng được viết bằng Python. Trong dự án này, Django sẽ được dùng để tạo một server web quản lý sinh viên. Server sẽ cung cấp các chức năng như quản lý thông tin sinh viên (thêm, sửa, xóa, và xem danh sách sinh viên) và tích hợp các công nghệ để giao tiếp với người dùng thông qua API.

### 2. Sử dụng Django Rest Framework (DRF) để tạo API
Django Rest Framework (DRF) là một thư viện mạnh mẽ hỗ trợ xây dựng các API RESTful trên nền tảng Django. Với DRF, bạn có thể dễ dàng tạo ra các endpoint API để thực hiện các thao tác như truy vấn, thêm mới, cập nhật, hoặc xóa dữ liệu sinh viên trong hệ thống. DRF cũng hỗ trợ nhiều tính năng như phân trang, xác thực, và quản lý quyền hạn, giúp xây dựng API một cách hiệu quả và dễ dàng.

### 3. Sử dụng JWT (Json Web Token) để xác thực người dùng
Json Web Token (JWT) là một phương thức hiện đại và an toàn để xác thực người dùng trong các ứng dụng web. Trong dự án này, JWT sẽ được tích hợp để quản lý việc đăng nhập và bảo mật các API. Người dùng sau khi đăng nhập thành công sẽ nhận được một token, token này sẽ được dùng trong các lần gửi yêu cầu tiếp theo để xác thực quyền truy cập. Phương pháp này đảm bảo rằng chỉ những người dùng hợp lệ mới có thể sử dụng các chức năng của hệ thống.

Với ba công nghệ này, hệ thống quản lý sinh viên sẽ đảm bảo tính năng mạnh mẽ, dễ sử dụng và bảo mật cao.