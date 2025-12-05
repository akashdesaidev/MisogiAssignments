package main

import (
	"context"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/akashdesaidev/MisogiAssignments/internal/config"
	"github.com/akashdesaidev/MisogiAssignments/internal/domain"
	"github.com/akashdesaidev/MisogiAssignments/internal/handlers"
	"github.com/akashdesaidev/MisogiAssignments/internal/repository"
	"github.com/akashdesaidev/MisogiAssignments/internal/service"
	"github.com/akashdesaidev/MisogiAssignments/pkg/logger"
	"go.uber.org/zap"
)

// @title           Go Production CRUD API
// @version         1.0
// @description     A production-ready CRUD application in Go.
// @host            localhost:8080
// @BasePath        /
func main() {
	// Load Configuration
	cfg, err := config.LoadConfig()
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	// Initialize Logger
	appLogger := logger.NewLogger(cfg.Logger.Level)
	defer appLogger.Sync()
	appLogger.Info("Starting application...")

	// Initialize Database
	db, err := repository.NewSQLiteDB(cfg.Database.File)
	if err != nil {
		appLogger.Fatal("Failed to connect to database", zap.Error(err))
	}

	// Auto Migration
	if err := db.AutoMigrate(&domain.Product{}); err != nil {
		appLogger.Fatal("Failed to migrate database", zap.Error(err))
	}

	// Initialize Layers
	productRepo := repository.NewProductRepository(db)
	productService := service.NewProductService(productRepo)
	router := handlers.NewRouter(appLogger, productService)

	// Server
	server := &http.Server{
		Addr:    ":" + cfg.Server.Port,
		Handler: router,
	}

	// Graceful Shutdown Channel
	done := make(chan os.Signal, 1)
	signal.Notify(done, os.Interrupt, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		if err := server.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			appLogger.Fatal("Server startup failed", zap.Error(err))
		}
	}()

	appLogger.Info("Server started", zap.String("port", cfg.Server.Port))

	<-done
	appLogger.Info("Server stopped")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := server.Shutdown(ctx); err != nil {
		appLogger.Fatal("Server forced to shutdown", zap.Error(err))
	}

	appLogger.Info("Server exited properly")
}
