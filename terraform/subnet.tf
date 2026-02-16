resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.main.id
  cidr_block = var.subnet_cidr

  availability_zone = "ap-south-1a"

  tags = {
    Name = "public-subnet"
  }
}