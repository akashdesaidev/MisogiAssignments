package repository

import (
	"context"
	"testing"

	"github.com/akashdesaidev/MisogiAssignments/internal/domain"
	"github.com/glebarez/sqlite"
	"github.com/stretchr/testify/assert"
	"gorm.io/gorm"
)

func setupTestDB() *gorm.DB {
	db, _ := gorm.Open(sqlite.Open("file::memory:?cache=shared"), &gorm.Config{})
	db.AutoMigrate(&domain.Product{})
	return db
}

func TestCreateGetProduct(t *testing.T) {
	db := setupTestDB()
	repo := NewProductRepository(db)
	ctx := context.Background()

	product := &domain.Product{
		Name:     "Integration Test Product",
		Price:    100.0,
		Quantity: 10,
	}

	err := repo.Create(ctx, product)
	assert.NoError(t, err)
	assert.NotZero(t, product.ID)

	fetched, err := repo.GetByID(ctx, product.ID)
	assert.NoError(t, err)
	assert.Equal(t, product.Name, fetched.Name)
}

func TestListProducts(t *testing.T) {
	db := setupTestDB()
	repo := NewProductRepository(db)
	ctx := context.Background()

	for i := 0; i < 5; i++ {
		repo.Create(ctx, &domain.Product{Name: "P", Price: 10, Quantity: 1})
	}

	products, total, err := repo.List(ctx, 0, 10)
	assert.NoError(t, err)
	assert.Equal(t, int64(5), total)
	assert.Len(t, products, 5)
}
