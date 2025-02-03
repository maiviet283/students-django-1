from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, RegexValidator
from django.core.validators import FileExtensionValidator
from django.utils.timezone import now
from phonenumber_field.modelfields import PhoneNumberField

class Classes(models.Model):
    name = models.CharField(
        max_length=5,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Z]\d{2}$',
                message="Tên lớp phải có định dạng chữ hoa + 2 số (VD: A01)"
            )
        ]
    )
    max_students = models.PositiveSmallIntegerField(
        verbose_name="Số lượng tối đa",
        validators=[MinValueValidator(50), MaxValueValidator(80)],
        help_text="Số lượng học sinh tối đa từ 50-80",
        null=True,
        blank=True
    )
    current_students = models.PositiveIntegerField(
        verbose_name="Số lượng hiện tại",
        default=0,
        editable=False
    )

    class Meta:
        verbose_name = "Lớp học"
        verbose_name_plural = "Các lớp học"
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.current_students}/{self.max_students})"

class Students(models.Model):
    GENDER_CHOICES = (
        ('M', 'Nam'),
        ('F', 'Nữ'),
        ('O', 'Khác')
    )

    avatar = models.ImageField(
        upload_to='students/avatars/%Y/%m/',
        verbose_name="Ảnh đại diện",
        blank=True,
        null=True,
        validators=[
            FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])
        ],
        default='students/avatars/default.png'
    )
    full_name = models.CharField(
        default="full name",
        max_length=150,
        verbose_name="Họ và tên"
    )
    date_of_birth = models.DateField(
        default="2000-01-01",
        verbose_name="Ngày sinh"
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        verbose_name="Giới tính"
    )
    student_class = models.ForeignKey(
        Classes,
        on_delete=models.PROTECT,
        related_name='students',
        verbose_name="Lớp học",
        null=True,
        blank=True
    )
    phone_number = PhoneNumberField(
        verbose_name="Số điện thoại",
        region='VN',
        unique=True
    )
    email = models.EmailField(
        verbose_name="Email",
        unique=True
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Địa chỉ"
    )
    username = models.CharField(
        max_length=20,
        unique=True,
        verbose_name="Tên đăng nhập"
    )
    password = models.CharField(
        max_length=128,
        verbose_name="Mật khẩu"
    )
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Học sinh"
        verbose_name_plural = "Danh sách học sinh"
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
        ]
        ordering = ['student_class', 'full_name']

    def __str__(self):
        return f"{self.full_name} ({self.student_class})"

class Book(models.Model):
    COVER_TYPES = (
        ('H', 'Bìa cứng'),
        ('P', 'Bìa mềm')
    )

    cover_image = models.ImageField(
        upload_to='books/covers/%Y/%m/',
        verbose_name="Bìa sách",
        blank=True,
        null=True,
        default='books/covers/default.jpg'
    )
    title = models.CharField(
        max_length=255,
        verbose_name="Tên sách",
        db_index=True,
        null=True,
        blank=True
    )
    author = models.CharField(
        max_length=255,
        verbose_name="Tác giả"
    )
    isbn = models.CharField(
        max_length=13,
        verbose_name="ISBN",
        unique=True,
        null=True,
        blank=True
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Giá tiền",
        validators=[MinValueValidator(0)]
    )
    quantity = models.PositiveIntegerField(
        verbose_name="Số lượng tồn kho",
        default=0
    )
    cover_type = models.CharField(
        max_length=1,
        choices=COVER_TYPES,
        verbose_name="Loại bìa",
        default='P'
    )
    publish_date = models.DateField(
        verbose_name="Ngày xuất bản",
        default=now().date
    )
    description = models.TextField(
        verbose_name="Mô tả",
        blank=True,
        default='Đang cập nhật'
    )

    class Meta:
        verbose_name = "Sách"
        verbose_name_plural = "Danh mục sách"
        ordering = ['-publish_date', 'title']
        constraints = [
            models.CheckConstraint(
                check=models.Q(quantity__gte=0),
                name="quantity_non_negative"
            )
        ]

    def __str__(self):
        return f"{self.title} - {self.author} ({self.price}₫)"