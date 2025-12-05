package service

import (
	"context"
	"errors"

	"github.com/akashdesaidev/MisogiAssignments/internal/domain"
)

type productService struct {
	repo domain.ProductRepository
}

func NewProductService(repo domain.ProductRepository) domain.ProductService {
	return &productService{repo: repo}
}

func (s *productService) CreateProduct(ctx context.Context, name string, price float64, quantity int) (*domain.Product, error) {
	if name == "" {
		return nil, errors.New("product name is required")
	}
	if price < 0 {
		return nil, errors.New("price cannot be negative")
	}
	if quantity < 0 {
		return nil, errors.New("quantity cannot be negative")
	}

	product := &domain.Product{
		Name:     name,
		Price:    price,
		Quantity: quantity,
	}

	if err := s.repo.Create(ctx, product); err != nil {
		return nil, err
	}

	return product, nil
}

func (s *productService) GetProduct(ctx context.Context, id uint) (*domain.Product, error) {
	return s.repo.GetByID(ctx, id)
}

func (s *productService) ListProducts(ctx context.Context, page, pageSize int) ([]domain.Product, int64, error) {
	if page < 1 {
		page = 1
	}
	if pageSize < 1 || pageSize > 100 {
		pageSize = 10
	}
	offset := (page - 1) * pageSize
	return s.repo.List(ctx, offset, pageSize)
}

func (s *productService) UpdateProduct(ctx context.Context, id uint, name string, price float64, quantity int) (*domain.Product, error) {
	product, err := s.repo.GetByID(ctx, id)
	if err != nil {
		return nil, err
	}

	if name != "" {
		product.Name = name
	}
	if price >= 0 {
		product.Price = price
	}
	if quantity >= 0 {
		product.Quantity = quantity
	}

	if err := s.repo.Update(ctx, product); err != nil {
		return nil, err
	}

	return product, nil
}

func (s *productService) DeleteProduct(ctx context.Context, id uint) error {
	return s.repo.Delete(ctx, id)
}
