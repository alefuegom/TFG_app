package alefuegom.tfg.model;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.Pattern;


@Entity
@Table(name="clientes")
public class Cliente extends BaseEntity{
	
	@NotBlank
	private String direccion;
	
	@NotBlank
	@Pattern(regexp = "[\\w]{2}[\\d]{22}")
	private String cuentaBancaria;
	
	@OneToOne(cascade= CascadeType.ALL)
	private Persona persona;

	public String getDireccion() {
		return direccion;
	}

	public void setDireccion(String direccion) {
		this.direccion = direccion;
	}

	public String getCuentaBancaria() {
		return cuentaBancaria;
	}

	public void setCuentaBancaria(String cuentaBancaria) {
		this.cuentaBancaria = cuentaBancaria;
	}

	public Persona getPersona() {
		return persona;
	}

	public void setPersona(Persona persona) {
		this.persona = persona;
	}
	
	
}
