package config

import (
	"log"
	"strings"

	"github.com/spf13/viper"
)

type Config struct {
	Server   ServerConfig
	Database DatabaseConfig
	Logger   LoggerConfig
}

type ServerConfig struct {
	Port string
	Mode string // debug, release
}

type DatabaseConfig struct {
	File string
}

type LoggerConfig struct {
	Level string // debug, info, warn, error
}

func LoadConfig() (*Config, error) {
	v := viper.New()

	v.SetConfigName(".env")
	v.SetConfigType("env")
	v.AddConfigPath(".")
	v.AutomaticEnv()
	v.SetEnvKeyReplacer(strings.NewReplacer(".", "_"))

	// Defaults
	v.SetDefault("SERVER_PORT", "8080")
	v.SetDefault("SERVER_MODE", "debug")
	v.SetDefault("DATABASE_FILE", "app.db")
	v.SetDefault("LOGGER_LEVEL", "info")

	if err := v.ReadInConfig(); err != nil {
		if _, ok := err.(viper.ConfigFileNotFoundError); !ok {
			return nil, err
		}
		// Config file not found; ignore error if desired, or log it
		log.Println("No .env file found, using defaults and environment variables")
	}

	var cfg Config
	cfg.Server.Port = v.GetString("SERVER_PORT")
	cfg.Server.Mode = v.GetString("SERVER_MODE")
	cfg.Database.File = v.GetString("DATABASE_FILE")
	cfg.Logger.Level = v.GetString("LOGGER_LEVEL")

	return &cfg, nil
}
