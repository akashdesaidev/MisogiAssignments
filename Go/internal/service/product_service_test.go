package service

import (
	"context"
	"testing"

	"github.com/akashdesaidev/MisogiAssignments/internal/domain"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/mock"
)

type MockProductRepository struct {
	mock.Mock
}

func (m *MockProductRepository) Create(ctx context.Context, product *domain.Product) error {
	args := m.Called(ctx, product)
	return args.Error(0)
}

func (m *MockProductRepository) GetByID(ctx context.Context, id uint) (*domain.Product, error) {
	args := m.Called(ctx, id)
	if args.Get(0) == nil {
		return nil, args.Error(1)
	}
	return args.Get(0).(*domain.Product), args.Error(1)
}

func (m *MockProductRepository) List(ctx context.Context, offset, limit int) ([]domain.Product, int64, error) {
	args := m.Called(ctx, offset, limit)
	return args.Get(0).([]domain.Product), args.Get(1).(int64), args.Error(2)
}

func (m *MockProductRepository) Update(ctx context.Context, product *domain.Product) error {
	args := m.Called(ctx, product)
	return args.Error(0)
}

func (m *MockProductRepository) Delete(ctx context.Context, id uint) error {
	args := m.Called(ctx, id)
	return args.Error(0)
}

func TestCreateProduct(t *testing.T) {
	mockRepo := new(MockProductRepository)
	service := NewProductService(mockRepo)
	ctx := context.Background()

	mockRepo.On("Create", ctx, mock.AnythingOfType("*domain.Product")).Return(nil)

	product, err := service.CreateProduct(ctx, "Test Product", 10.0, 5)

	assert.NoError(t, err)
	assert.NotNil(t, product)
	assert.Equal(t, "Test Product", product.Name)
	assert.Equal(t, 10.0, product.Price)
	assert.Equal(t, 5, product.Quantity)

	mockRepo.AssertExpectations(t)
}

func TestCreateProductInvalidInput(t *testing.T) {
	mockRepo := new(MockProductRepository)
	service := NewProductService(mockRepo)
	ctx := context.Background()

	_, err := service.CreateProduct(ctx, "", 10.0, 5)
	assert.Error(t, err)
	assert.Equal(t, "product name is required", err.Error())

	_, err = service.CreateProduct(ctx, "Test", -1.0, 5)
	assert.Error(t, err)
	assert.Equal(t, "price cannot be negative", err.Error())
}
