-- Criação do banco de dados para sistema de gerenciamento escolar infantil
CREATE DATABASE IF NOT EXISTS escola_infantil;
USE escola_infantil;

-- Tabela Professor: Armazena informações dos professores
CREATE TABLE Professor (
  id_professor INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único do professor',
  nome_completo VARCHAR(255) NOT NULL COMMENT 'Nome completo do professor',
  email VARCHAR(100) COMMENT 'E-mail de contato do professor',
  telefone VARCHAR(20) COMMENT 'Telefone de contato do professor'
) ENGINE=InnoDB;

-- Tabela Turma: Representa as turmas da escola
CREATE TABLE Turma (
  id_turma INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único da turma',
  nome_turma VARCHAR(50) NOT NULL COMMENT 'Nome identificador da turma',
  id_professor INT COMMENT 'Professor responsável pela turma',
  horario VARCHAR(100) COMMENT 'Horário de funcionamento da turma',
  FOREIGN KEY (id_professor) REFERENCES Professor(id_professor) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Tabela Aluno: Armazena informações dos alunos
CREATE TABLE Aluno (
  id_aluno INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único do aluno',
  nome_completo VARCHAR(255) NOT NULL COMMENT 'Nome completo do aluno',
  data_nascimento DATE NOT NULL COMMENT 'Data de nascimento do aluno',
  id_turma INT COMMENT 'Turma à qual o aluno pertence',
  nome_responsavel VARCHAR(255) NOT NULL COMMENT 'Nome do responsável legal',
  telefone_responsavel VARCHAR(20) NOT NULL COMMENT 'Telefone do responsável',
  email_responsavel VARCHAR(100) COMMENT 'E-mail do responsável',
  informacoes_adicionais TEXT COMMENT 'Informações adicionais sobre o aluno',
  FOREIGN KEY (id_turma) REFERENCES Turma(id_turma) ON DELETE SET NULL
) ENGINE=InnoDB;

-- Tabela Pagamento: Registra os pagamentos realizados
CREATE TABLE Pagamento (
  id_pagamento INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único do pagamento',
  id_aluno INT NOT NULL COMMENT 'Aluno vinculado ao pagamento',
  data_pagamento DATE NOT NULL COMMENT 'Data em que o pagamento foi realizado',
  valor_pago DECIMAL(10, 2) NOT NULL COMMENT 'Valor do pagamento',
  forma_pagamento VARCHAR(50) NOT NULL COMMENT 'Forma de pagamento utilizada',
  referencia VARCHAR(100) NOT NULL COMMENT 'Referência/descrição do pagamento',
  status VARCHAR(20) NOT NULL COMMENT 'Status do pagamento (Pago, Pendente, etc.)',
  FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela Presenca: Registra a frequência dos alunos
CREATE TABLE Presenca (
  id_presenca INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único do registro de presença',
  id_aluno INT NOT NULL COMMENT 'Aluno referenciado',
  data_presenca DATE NOT NULL COMMENT 'Data da aula/referência',
  presente BOOLEAN NOT NULL COMMENT 'Indica se o aluno estava presente',
  FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela Atividade: Armazena as atividades realizadas
CREATE TABLE Atividade (
  id_atividade INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único da atividade',
  descricao TEXT NOT NULL COMMENT 'Descrição da atividade',
  data_realizacao DATE NOT NULL COMMENT 'Data de realização da atividade'
) ENGINE=InnoDB;

-- Tabela Atividade_Aluno: Relacionamento muitos-para-muitos entre Atividade e Aluno
CREATE TABLE Atividade_Aluno (
  id_atividade INT NOT NULL COMMENT 'Referência à atividade',
  id_aluno INT NOT NULL COMMENT 'Referência ao aluno',
  PRIMARY KEY (id_atividade, id_aluno),
  FOREIGN KEY (id_atividade) REFERENCES Atividade(id_atividade) ON DELETE CASCADE,
  FOREIGN KEY (id_aluno) REFERENCES Aluno(id_aluno) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Tabela Usuario: Armazena os usuários do sistema
CREATE TABLE Usuario (
  id_usuario INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Identificador único do usuário',
  login VARCHAR(50) UNIQUE NOT NULL COMMENT 'Login de acesso',
  senha VARCHAR(255) NOT NULL COMMENT 'Senha criptografada',
  nivel_acesso VARCHAR(20) NOT NULL COMMENT 'Nível de acesso (admin, secretaria, professor)',
  id_professor INT COMMENT 'Vinculo com professor, se aplicável',
  FOREIGN KEY (id_professor) REFERENCES Professor(id_professor) ON DELETE SET NULL
) ENGINE=InnoDB;