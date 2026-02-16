resource "aws_instance" "web" {
  ami           = "ami-0f5ee92e2d63afc18"  # Amazon Linux (ap-south-1)
  instance_type = var.instance_type
  subnet_id     = aws_subnet.public.id
  security_groups = [aws_security_group.web_sg.id]

  tags = {
    Name = "Web-Server"
  }
}