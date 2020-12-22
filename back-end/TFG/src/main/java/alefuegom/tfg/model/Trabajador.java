package alefuegom.tfg.model;

import javax.persistence.CascadeType;
import javax.persistence.Entity;
import javax.persistence.JoinColumn;
import javax.persistence.OneToOne;
import javax.persistence.Table;
import javax.validation.constraints.NotBlank;

@Entity
@Table(name="trabajadores")
public class Trabajador extends BaseEntity{
	
	@NotBlank
	private String cualificacion;
	
	@OneToOne(cascade= CascadeType.ALL)
	private Persona persona;

	public String getCualificacion() {
		return cualificacion;
	}

	public void setCualificacion(String cualificacion) {
		this.cualificacion = cualificacion;
	}

	public Persona getPersona() {
		return persona;
	}
		
	public void setPersona(Persona persona) {
		this.persona = persona;
	}
	
	
}
