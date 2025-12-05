package domain

import (
	"context"
	"time"

	"gorm.io/gorm"
)

type Product struct {
	ID        uint           `gorm:"primaryKey" json:"id"`
	Name      string         `gorm:"size:255;not null" json:"name"`
	Price     float64        `gorm:"not null" json:"price"`
	Quantity  int            `gorm:"not null" json:"quantity"`
	CreatedAt time.Time      `json:"created_at"`
	UpdatedAt time.Time      `json:"updated_at"`
	DeletedAt gorm.DeletedAt `gorm:"index" json:"-"`
}

type ProductRepository interface {
	Create(ctx context.Context, product *Product) error
	GetByID(ctx context.Context, id uint) (*Product, error)
	List(ctx context.Context, offset, limit int) ([]Product, int64, error)
	Update(ctx context.Context, product *Product) error
	Delete(ctx context.Context, id uint) error
}

type ProductService interface {
	CreateProduct(ctx context.Context, name string, price float64, quantity int) (*Product, error)
	GetProduct(ctx context.Context, id uint) (*Product, error)
	ListProducts(ctx context.Context, page, pageSize int) ([]Product, int64, error)
	UpdateProduct(ctx context.Context, id uint, name string, price float64, quantity int) (*Product, error)
	DeleteProduct(ctx context.Context, id uint) error
}
